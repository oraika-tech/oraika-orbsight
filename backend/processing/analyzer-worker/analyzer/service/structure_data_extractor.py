import logging
import re
import string
from typing import Any, Dict, List, Optional, Tuple, Set
from uuid import UUID

import nltk
from langdetect import LangDetectException, detect
from nltk import word_tokenize
from nltk.corpus import stopwords
from pydantic import BaseSettings, Field, PrivateAttr

from analyzer.model.structure_data_request import StructuredData, UnstructuredDataRequest
from analyzer.model.taxonomy_data import TaxonomyData
from analyzer.persistence.db_entity_manager import DBEntityManager
from analyzer.service.tiyaro_api import TiyaroClient

HTTP_REGEX = r'http\S+'
MENTION_REGEX = "@[A-Za-z0-9_]+"
HASHTAGS_REGEX = "#[A-Za-z0-9_]+"

logger = logging.getLogger(__name__)


class StructuredDataExtractor(BaseSettings):
    # DB Entity Manager
    _db_entity_manager: DBEntityManager = PrivateAttr()

    # Text cleaning
    regex_substitute = " "
    http_regex = re.compile(HTTP_REGEX)
    mention_regex = re.compile(MENTION_REGEX)
    hashtags_regex = re.compile(HASHTAGS_REGEX)

    # Text tokenizer
    tokenizer_name = "punkt"

    # Token cleaning functions
    stop_words: Optional[List[str]]
    stop_words_language = 'english'

    # Classification API
    api_client = TiyaroClient()

    min_text_len: int = Field(20, env="MIN_TEXT_LENGTH")
    min_probability_level: float = Field(0.8, env="MINIMUM_PROBABILITY_LEVEL")
    min_tokens: int = Field(3, env="MINIMUM_TOKENS")

    # TODO: probably get it from tenant config table
    # This is orbsight internal, if tenant require data in other language then a translation can be added to their
    # desire language
    supported_lang_codes: List[str] = Field(["en"], env="SUPPORTED_LANG_CODES")
    emotion_labels: List[str] = Field(["positive", "negative", "neutral"], env="EMOTION_LABELS")

    def __init__(self, **data: Any):
        super().__init__(**data)
        try:
            nltk.data.find(f"tokenizers/{self.tokenizer_name}")
        except LookupError:
            nltk.download(f"{self.tokenizer_name}")

        if not self.stop_words:
            try:
                nltk.data.find("stopwords")
            except LookupError:
                nltk.download("stopwords")
            self.stop_words = stopwords.words(self.stop_words_language)

        self._db_entity_manager = DBEntityManager()

    # Clean text
    def _clean_text(self, text: str) -> str:
        cleaned_text = self.http_regex.sub(self.regex_substitute, text)
        cleaned_text = self.mention_regex.sub(self.regex_substitute, cleaned_text)
        cleaned_text = self.hashtags_regex.sub(self.regex_substitute, cleaned_text)
        return cleaned_text.strip()

    # Translate to English
    def _translate_text(self, text: str) -> str:
        return self.api_client.translate_text(text)

    # Create tokens
    def _tokenize_text(self, text: str) -> List[str]:
        # Remove stop words from tokens
        def _remove_stop_words(tokens: List[str]) -> List[str]:
            if not self.stop_words:
                return tokens
            return [token for token in tokens if token not in self.stop_words]

        # Remove punctuation from tokens
        def _remove_punctuation(tokens: List[str]) -> List[str]:
            return [
                token.translate(token.maketrans("", "", string.punctuation))  # type: ignore
                for token in tokens
                if len(token.translate(token.maketrans("", "", string.punctuation)))  # type: ignore
            ]

        # Remove white space from tokens
        def _remove_white_space(tokens: List[str]) -> List[str]:
            striped_tokens = [token.strip() for token in tokens]
            return [token for token in striped_tokens if token != ""]

        # Change token case to lower
        def _to_lower(tokens: List[str]) -> List[str]:
            return [token.lower() for token in tokens]

        tokenized_tokens = word_tokenize(text)
        tokenized_tokens = _remove_stop_words(tokenized_tokens)
        tokenized_tokens = _remove_punctuation(tokenized_tokens)
        tokenized_tokens = _remove_white_space(tokenized_tokens)
        tokenized_tokens = _to_lower(tokenized_tokens)
        return tokenized_tokens

    # Extract taxonomy via keywords
    def _extract_keywords(self, text: str, tenant_id: UUID) -> TaxonomyData:
        taxonomy_df = self._db_entity_manager.get_taxonomy_dataframe(tenant_id)

        taxonomy_df['Search'] = [
            re.search(r'\b{}\b'.format(re.escape(x)), text, re.IGNORECASE) is not None for x in taxonomy_df['keyword']
        ]

        keywords_present_df = taxonomy_df[taxonomy_df['Search'] == True]

        keywords_found = keywords_present_df.shape[0]

        if keywords_found > 0:
            terms: Set[str] = set()
            tags: Set[str] = set()

            for terms_string in set(keywords_present_df['term'].to_list()):
                if terms_string is not None and terms_string != "":
                    terms.add(terms_string)

            for tags_string in set(keywords_present_df['tags'].to_list()):
                if tags_string is not None and tags_string != "":
                    tags.update(tags_string.split(","))

            return TaxonomyData(
                tags=tags,
                terms=terms
            )

        return TaxonomyData()

    # Emotion detection
    def _emotion_classification(self, text: str, labels: List[str]) -> Tuple[str, float]:
        classifier_response = self.api_client.classify_text(
            text=text,
            labels=labels,
            multi_label=False
        )

        emotion, value = next(iter(classifier_response.items()))
        return emotion, value

    # Classification
    def _classify_text(self, text: str, labels: List[str], multi_label: bool = True) -> Dict[str, float]:
        category_map = self.api_client.classify_text(
            text=text,
            labels=labels,
            multi_label=multi_label
        )
        return dict(sorted(category_map.items(), key=lambda x: x[1], reverse=True))

    # Detect Language
    def _language_detection(self, text: str) -> Optional[str]:
        try:
            return detect(text)
        except LangDetectException as ex:
            logger.error(f"Error in language detection of `{text}`: {ex}")
            return None

    def _get_categories(self, tenant_id) -> List[str]:
        return self._db_entity_manager.get_categories(tenant_id)

    def extract_structure(self, data_request: UnstructuredDataRequest) -> StructuredData:
        # TODO: Extract, Emojis, URL, Currency, Hashtags, Mention
        # TODO: Expend hashtags and emojis

        # Clean text (Remove URL, mention, blank lines, white spaces, Hashtags)
        clean_text = self._clean_text(data_request.raw_text)

        structured_data: StructuredData
        # Check length of string
        if len(clean_text) > self.min_text_len:
            # Detect language
            text_language = self._language_detection(clean_text)

            # If language is not in SUPPORTED_LANG_CODES then translate it
            # TODO: store processed_text so in future no need for translation and cleaning again
            #  incase if reclassification is required if user add or update categories
            if text_language not in self.supported_lang_codes:
                processed_text = self._translate_text(clean_text)
            else:
                processed_text = clean_text

            # Extract taxonomy data
            taxonomy_data = self._extract_keywords(processed_text, data_request.tenant_id)

            # Tokenize text and clean tokens
            tokens = self._tokenize_text(processed_text)

            # Check number of tokens to take decision whether to classify or not
            very_small_text = len(tokens) < self.min_tokens

            # Categories to classify and detect emotions
            classification_labels = self._get_categories(data_request.tenant_id) + self.emotion_labels

            # Classify text into categories
            classified_categories: List[str] = []
            text_emotion = "undetermined"
            if not very_small_text and len(classification_labels) > 0:
                classifier_map = self._classify_text(processed_text, classification_labels)
                classified_categories = [
                    category
                    for category, probability in classifier_map.items()
                    if probability > self.min_probability_level
                ]

                for emotion in self.emotion_labels:
                    if emotion in classified_categories:
                        if text_emotion == "undetermined":
                            text_emotion = emotion
                        classified_categories.remove(emotion)

            # Create structured data map from all the above process and incoming request data
            structured_data = StructuredData(
                tags=list(taxonomy_data.tags),
                terms=list(taxonomy_data.terms),
                categories=classified_categories,
                emotion=text_emotion,
                text_length=len(data_request.raw_text),
                text_language=text_language,
                remark="VERY_SMALL_TEXT" if very_small_text else None,
            )
        else:
            structured_data = StructuredData(
                text_length=len(data_request.raw_text),
                remark="VERY_SMALL_TEXT"
            )

        return structured_data
