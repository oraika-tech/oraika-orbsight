import logging
import re
from typing import List, Optional, Tuple, Dict, Any

import string
import nltk
from langdetect import detect, LangDetectException
from nltk import word_tokenize
from nltk.corpus import stopwords
from pydantic import BaseSettings, Field

from analyzer.model.structure_data_request import UnstructuredDataRequest, StructuredData
from analyzer.service.entity_extractor import EntityExtractor
from analyzer.model.entity_data import EntityData
from analyzer.service.tiyaro_api import TiyaroClient

HTTP_REGEX = r'http\S+'
MENTION_REGEX = "@[A-Za-z0-9_]+"
HASHTAGS_REGEX = "#[A-Za-z0-9_]+"

# TODO: Currently hardcoded, it should be dependent on company
NEGATIVE_CLASSIFICATION_LABELS = ["fraud", "complaint", "harassment", "charges", "access", "delay", "interface"]
EMOTION_LABELS = ["positive", "negative"]
NEGATIVE_EMOTIONS = ["negative", "sarcasm"]

# TODO: Make it configurable
MINIMUM_TOKENS = 3
MINIMUM_PROBABILITY_LEVEL = 0.6

# This is Obsights internal, if company require data in other language then a translation can be added to their desire
# language
SUPPORTED_LANG_CODES = ["en"]

logger = logging.getLogger(__name__)


class StructuredDataExtractor(BaseSettings):
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

    # Entity Extractor
    entity_extractor = EntityExtractor()

    # Classification API
    api_client = TiyaroClient()

    min_text_len: int = Field(20, env="MIN_TEXT_LENGTH")

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

    # Extract entities via keywords
    def _extract_entities(self, tokens: List[str], entity_owner_id: int) -> EntityData:
        return self.entity_extractor.extract_entities(tokens, entity_owner_id)

    # Emotion detection
    def _emotion_classification(self, text: str, labels: Optional[List[str]] = None) -> Tuple[str, float]:
        labels = labels or EMOTION_LABELS
        classifier_response = self.api_client.classify_text(
            text=text,
            labels=labels,
            multi_label=False
        )

        emotion, value = next(iter(classifier_response.items()))
        return emotion, value

    # Classification
    def _classify_text(self, text: str, labels: List[str], multi_label: bool = True) -> Dict[str, float]:
        return self.api_client.classify_text(
            text=text,
            labels=labels,
            multi_label=multi_label
        )

    # Detect Language
    def _language_detection(self, text: str) -> Optional[str]:
        try:
            return detect(text)
        except LangDetectException as ex:
            logger.error(f"Error in language detection of `{text}`: {ex}")
            return None

    def extract_structure_slow(self, data_request: UnstructuredDataRequest) -> StructuredData:
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
            if text_language is not None and text_language not in SUPPORTED_LANG_CODES:
                processed_text = self._translate_text(clean_text)
            else:
                processed_text = clean_text

            # TODO: store processed_text so in future no need for translation and cleaning again
            #  incase if reclassification is required if user add or update categories

            # Tokenize text and clean tokens
            tokens = self._tokenize_text(processed_text)

            # Extract entity data
            entity_data = self._extract_entities(tokens, data_request.company_id)

            # Check number of tokens to take decision whether to classify or not
            very_small_text = len(tokens) < MINIMUM_TOKENS

            # Emotion detection
            # TODO: For small text even dictionary based small sentiment detector (like VADER) can also be used
            # TODO: Get emotions list from company_id if they provided
            text_emotion, text_emotion_prob = self._emotion_classification(processed_text, EMOTION_LABELS)

            # Find categories to classify text based one emotion and entity
            # TODO: Handle positive emotion case
            if text_emotion in NEGATIVE_EMOTIONS:
                classification_labels = list(entity_data.categories)
                # TODO: Ideally it should not reach at this level but adding check for hygiene purpose
                if len(classification_labels) == 0:
                    classification_labels = NEGATIVE_CLASSIFICATION_LABELS
            else:
                classification_labels = []

            # Classify text into categories
            classified_categories: List[str] = []
            if not very_small_text and len(classification_labels) > 0:
                classifier_map = self._classify_text(processed_text, classification_labels)
                classified_categories = [
                    category
                    for category, probability in classifier_map.items()
                    if probability > MINIMUM_PROBABILITY_LEVEL
                ]

            # Create structured data map from all the above process and incoming request data
            # TODO: Move to proper place, currently difficult to map DB column name and dictionary key name
            structured_data = StructuredData(
                entity_data={
                    entity: list(entity_vals)
                    for entity, entity_vals in entity_data.entity_map.items()
                } if entity_data.entity_map else {},
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

    def extract_structure_fast(self, data_request: UnstructuredDataRequest) -> StructuredData:
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
            if text_language not in SUPPORTED_LANG_CODES:
                processed_text = self._translate_text(clean_text)
            else:
                processed_text = clean_text

            # TODO: store processed_text so in future no need for translation and cleaning again
            #  incase if reclassification is required if user add or update categories

            # Tokenize text and clean tokens
            tokens = self._tokenize_text(processed_text)

            # Extract entity data
            entity_data = self._extract_entities(tokens, data_request.company_id)

            # Check number of tokens to take decision whether to classify or not
            very_small_text = len(tokens) < MINIMUM_TOKENS

            # Categories to classify and detect emotions
            classification_labels = NEGATIVE_CLASSIFICATION_LABELS + EMOTION_LABELS

            # Classify text into categories
            classified_categories: List[str] = []
            text_emotion = "positive"
            if not very_small_text and len(classification_labels) > 0:
                classifier_map = self._classify_text(processed_text, classification_labels)
                classified_categories = [
                    category
                    for category, probability in classifier_map.items()
                    if probability > MINIMUM_PROBABILITY_LEVEL
                ]

                if "negative" in classified_categories:
                    text_emotion = "negative"
                    if "positive" in classified_categories:
                        classified_categories.remove("positive")

            # Create structured data map from all the above process and incoming request data
            # TODO: Move to proper place, currently difficult to map DB column name and dictionary key name
            structured_data = StructuredData(
                entity_data={
                    entity: list(entity_vals)
                    for entity, entity_vals in entity_data.entity_map.items()
                } if entity_data.entity_map else {},
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
