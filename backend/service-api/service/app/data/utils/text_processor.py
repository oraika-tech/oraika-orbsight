import logging
import re
import string
from typing import List, Dict, Pattern

from nltk import word_tokenize

from service.app.data.utils.stop_words_utils import StopWordUtility
from service.app.data.utils.text_utils import get_control_char_regex, get_rakun_keyphrase_detector

logger = logging.getLogger(__name__)

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

# Text cleaning
regex_substitute: str = " "
http_regex: Pattern[str] = re.compile(r'http\S+')
mention_regex: Pattern[str] = re.compile("@[A-Za-z0-9_]+")
hashtags_regex: Pattern[str] = re.compile("#[A-Za-z0-9_]+")
digits_regex: Pattern[str] = re.compile(r"\d")

punctuations: List[str] = list(r'''!()-[]{};:'"\,<>./?@#$%^&*_~''')
control_char_regex = get_control_char_regex()
_rakun_model = get_rakun_keyphrase_detector()
swu = StopWordUtility()


def remove_punctuations(text: str) -> str:
    return text.translate(str.maketrans('', '', string.punctuation + '›·'))


def clean_text(text: str, deep_clean: bool = False, lang_code: str = 'en') -> str:
    cleaned_text = http_regex.sub(regex_substitute, text)
    cleaned_text = mention_regex.sub(regex_substitute, cleaned_text)
    # cleaned_text = hashtags_regex.sub(regex_substitute, cleaned_text)
    cleaned_text = digits_regex.sub(regex_substitute, cleaned_text)
    cleaned_text = remove_punctuations(cleaned_text)

    cleaned_text = cleaned_text.strip()
    if deep_clean:
        if control_char_regex:
            cleaned_text = control_char_regex.sub(regex_substitute, cleaned_text)
        if cleaned_text in punctuations or cleaned_text in get_stop_words(lang_code):
            return ""

    return cleaned_text.strip()


def get_stop_words(lang_code='en'):
    return swu.stop_words[LANG_CODE_TO_NAME.get(lang_code)]


def tokenize_text(text: str, lang_code='en') -> List[str]:
    # Remove stop words from tokens
    def _remove_stop_words(tokens: List[str], lang='english') -> List[str]:
        if not swu.stop_words[lang]:
            return tokens
        return [token for token in tokens if token not in swu.stop_words[lang]]

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


def extract_key_phrases(text: str) -> Dict[str, float]:
    return _keyword_by_rakun(text)


def _keyword_by_rakun(text: str) -> Dict[str, float]:
    key_phrases = _rakun_model.find_keywords(text, input_type="string")
    if not key_phrases:
        return {}
    return {key_phrase: distance for key_phrase, distance in key_phrases}
