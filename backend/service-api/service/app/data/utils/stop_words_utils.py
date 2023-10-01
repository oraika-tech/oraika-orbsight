import logging
from pathlib import Path
from typing import Dict, Set, Optional

import nltk
import stopwordsiso
from nltk.corpus import stopwords

logger = logging.getLogger(__name__)


class StopWordUtility:
    _stop_words: Optional[Dict[str, Set[str]]] = None

    @property
    def stop_words(self):
        if not self._stop_words:
            self._nltk_download()
            self._stop_words = self._get_stop_words()
        return self._stop_words

    @staticmethod
    def _nltk_download():
        tokenizer_name = "punkt"
        try:
            nltk.data.find(f"tokenizers/{tokenizer_name}")
        except LookupError:
            nltk.download(f"{tokenizer_name}")

        try:
            nltk.data.find("stopwords")
        except LookupError:
            nltk.download("stopwords")

    @staticmethod
    def _get_stop_words() -> Dict[str, Set[str]]:
        _stop_words: Dict[str, Set[str]] = {}
        hinglish_stop_file: str = "../assets/hinglish_stopwords"
        FILE_PATH = Path(__file__).parent

        LANGUAGES = [
            "english", "hindi", "tamil", "telugu", "gujarati", "kannada",
            "bengali", "marathi", "malayalam", "punjabi", "urdu", "nepali"
        ]
        for language in LANGUAGES:
            try:
                if stopwordsiso.has_lang(language):
                    _stop_words[language] = set(stopwords.words(language) + stopwordsiso.stopwords(language))
                else:
                    _stop_words[language] = set(stopwords.words(language))
            except Exception as e:
                logger.error(f"Error processing language {language}: {e}")
                _stop_words[language] = set()

        with open(FILE_PATH / hinglish_stop_file, encoding='utf-8') as f:
            lines = f.readlines()
            extra_stop_list = [line.strip() for line in lines]

        # Combine hindi and english
        _stop_words['english'].update(extra_stop_list)
        _stop_words['english'].update(_stop_words['hindi'])
        _stop_words['hindi'] = _stop_words['english']
        return _stop_words
