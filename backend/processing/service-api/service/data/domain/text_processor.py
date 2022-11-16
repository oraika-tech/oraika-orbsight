import re
import sys
from enum import Enum

import unicodedata
from pathlib import Path
from typing import List, Any, Dict, Optional, Set, Pattern

import nltk
import stopwordsiso
from nltk import word_tokenize
from nltk.corpus import stopwords
from pydantic import BaseSettings, Field, PrivateAttr
from rakun2 import RakunKeyphraseDetector

HTTP_REGEX = r'http\S+'
MENTION_REGEX = "@[A-Za-z0-9_]+"
HASHTAGS_REGEX = "#[A-Za-z0-9_]+"
DIGITS_REGEX = r"\d"

LANGUAGES = [
    "english", "hindi", "tamil", "telugu", "gujarati", "kannada",
    "bengali", "marathi", "malayalam", "punjabi", "urdu", "nepali"
]

LANG_CODE_TO_NAME = {
    "en": "english",
    "hi": "hindi",
    "ta": "tamil",
    "te": "telugu",
    "gu": "gujarati",
    "kn": "kannada",
    "bn": "bengali",
    "mr": "marathi",
    "ml": "malayalam",
    "pa": "punjabi",
    "ur": "urdu",
}


class KeywordExtractorType(int, Enum):
    KeyBert = 1
    Rakun = 2


FILE_PATH = Path(__file__).parent


class TextProcessor(BaseSettings):
    _rakun_model: RakunKeyphraseDetector = PrivateAttr()

    # Text cleaning
    regex_substitute: str = " "
    http_regex: Pattern[str] = re.compile(HTTP_REGEX)
    mention_regex: Pattern[str] = re.compile(MENTION_REGEX)
    hashtags_regex: Pattern[str] = re.compile(HASHTAGS_REGEX)
    digits_regex: Pattern[str] = re.compile(DIGITS_REGEX)
    control_char_regex: Optional[Any]

    # Text tokenizer
    tokenizer_name: str = "punkt"

    punctuations: List[str] = list('''!()-[]{};:'"\,<>./?@#$%^&*_~''')

    # Token cleaning functions
    stop_words: Dict[str, Set[str]] = {}
    hinglish_stop_file: str = "asset/hinglish_stopwords"

    # Keyphrases
    keyword_extractor: KeywordExtractorType = Field(KeywordExtractorType.Rakun, env='KEYWORD_EXTRACTOR')
    max_keyphrases: int = Field(16, env='MAXIMUM_KEY_PHRASES')
    # Rakun Param
    merge_threshold: float = 1.1
    alpha: float = 0.3
    token_prune_len: int = 3

    def __init__(self, **data: Any):
        super().__init__(**data)
        try:
            nltk.data.find(f"tokenizers/{self.tokenizer_name}")
        except LookupError:
            nltk.download(f"{self.tokenizer_name}")

        try:
            nltk.data.find("stopwords")
        except LookupError:
            nltk.download("stopwords")
        for language in LANGUAGES:
            try:
                if stopwordsiso.has_lang(language):
                    self.stop_words[language] = set(stopwords.words(language) + stopwordsiso.stopwords(language))
                else:
                    self.stop_words[language] = set(stopwords.words(language))
            except:
                self.stop_words[language] = set()

        extra_stop_list = []
        with open(FILE_PATH / self.hinglish_stop_file, encoding='utf-8') as f:
            lines = f.readlines()
            extra_stop_list = [line.strip() for line in lines]

        # Combine hindi and english
        self.stop_words['english'].update(extra_stop_list)
        self.stop_words['english'].update(self.stop_words['hindi'])
        self.stop_words['hindi'] = self.stop_words['english']

        if not self.control_char_regex:
            # Get all unicode characters
            all_chars = (chr(i) for i in range(sys.maxunicode))
            # Get all non printable characters
            control_chars = ''.join(c for c in all_chars if unicodedata.category(c) == 'Cc')
            # Create regex of above characters
            self.control_char_regex = re.compile('[%s]' % re.escape(control_chars))

        hyper_parameters = {
            "num_keywords": self.max_keyphrases,
            "merge_threshold": self.merge_threshold,
            "alpha": self.alpha,
            "token_prune_len": self.token_prune_len
        }
        self._rakun_model = RakunKeyphraseDetector(hyper_parameters)

    def clean_text(self, text: str, deep_clean: bool = False, lang_code: str = 'en') -> str:
        cleaned_text = self.http_regex.sub(self.regex_substitute, text)
        cleaned_text = self.mention_regex.sub(self.regex_substitute, cleaned_text)
        # cleaned_text = self.hashtags_regex.sub(self.regex_substitute, cleaned_text)
        cleaned_text = self.digits_regex.sub(self.regex_substitute, cleaned_text)

        cleaned_text = cleaned_text.strip()
        if deep_clean:
            cleaned_text = self.control_char_regex.sub(self.regex_substitute, cleaned_text)
            if cleaned_text in self.punctuations or cleaned_text in self.get_stop_words(lang_code):
                return ""

        return cleaned_text.strip()

    def get_stop_words(self, lang_code='en'):
        return self.stop_words[LANG_CODE_TO_NAME.get(lang_code)]

    def tokenize_text(self, text: str, lang_code='en') -> List[str]:
        # Remove stop words from tokens
        def _remove_stop_words(tokens: List[str], lang='english') -> List[str]:
            if not self.stop_words[lang]:
                return tokens
            return [token for token in tokens if token not in self.stop_words[lang]]

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

        lang_name = LANG_CODE_TO_NAME.get(lang_code)
        tokenized_tokens = word_tokenize(text)
        tokenized_tokens = _remove_stop_words(tokenized_tokens, lang_name)
        tokenized_tokens = _remove_punctuation(tokenized_tokens)
        tokenized_tokens = _remove_white_space(tokenized_tokens)
        tokenized_tokens = _to_lower(tokenized_tokens)
        return tokenized_tokens

    def extract_key_phrases(self, text: str, remove_stopwords: bool = False, lang_code: str = 'en') -> Dict[str, float]:
        # if self.keyword_extractor == KeywordExtractorType.KeyBert:
        #    return self._keyword_by_keybert(text, remove_stopwords, lang_code)
        return self._keyword_by_rakun(text)

    def _keyword_by_rakun(self, text: str) -> Dict[str, float]:
        key_phrases = self._rakun_model.find_keywords(text, input_type="string")
        if key_phrases is None or len(key_phrases) == 0:
            return {}
        return {key_phrase: distance for key_phrase, distance in key_phrases}

    # Keeping old code in case we need it
    # from keybert import KeyBERT
    # _keybert_model: KeyBERT = PrivateAttr()
    #
    # # KeyBert Param
    # key_phrase_model_name: str = Field("paraphrase-multilingual-MiniLM-L12-v2", env='KEY_PHRASE_MODEL')
    # min_ngrams: int = Field(1, env='MAXIMUM_NGRAMS')
    # max_ngrams: int = Field(3, env='MAXIMUM_NGRAMS')
    # use_mmr: bool = True  # Maximal Margin Relevance (MMR)
    # keyphrase_diversity: float = Field(
    #     0.25, ge=0.0, le=1.0
    # )  # Keyphrases diversity only application if user_mmr is True
    #
    # _keybert_model = KeyBERT(key_phrase_model_name)
    #
    # def _keyword_by_keybert(self, text: str, remove_stopwords: bool = False, lang_code: str = 'en') -> Dict[str, float]:
    #
    #     key_phrases = self._keybert_model.extract_keywords(
    #         text,
    #         keyphrase_ngram_range=(self.min_ngrams, self.max_ngrams),
    #         use_mmr=self.use_mmr,
    #         stop_words=list(self.get_stop_words(lang_code)) if remove_stopwords else None,
    #         top_n=self.max_keyphrases,
    #         diversity=self.keyphrase_diversity,
    #     )
    #
    #     if key_phrases is None or len(key_phrases) == 0:
    #         return {}
    #
    #     key_phrases_list = key_phrases[0] if isinstance(key_phrases[0], List) else key_phrases
    #
    #     return {key_phrase: distance for key_phrase, distance in key_phrases_list}
