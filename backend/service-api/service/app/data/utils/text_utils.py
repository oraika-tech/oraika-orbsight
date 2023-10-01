import logging
import re
import sys
import unicodedata

from rakun2 import RakunKeyphraseDetector

from service.common.config.app_settings import app_settings

logger = logging.getLogger(__name__)


def get_control_char_regex():
    # Get all unicode characters
    all_chars = (chr(i) for i in range(sys.maxunicode))
    # Get all non printable characters
    control_chars = ''.join(c for c in all_chars if unicodedata.category(c) == 'Cc')
    # Create regex of above characters
    return re.compile('[%s]' % re.escape(control_chars))


def get_rakun_keyphrase_detector() -> RakunKeyphraseDetector:
    max_keyphrases = app_settings.MAXIMUM_KEY_PHRASES
    merge_threshold = 1.1
    alpha = 0.3
    token_prune_len = 3
    hyper_parameters = {
        "num_keywords": max_keyphrases,
        "merge_threshold": merge_threshold,
        "alpha": alpha,
        "token_prune_len": token_prune_len
    }
    return RakunKeyphraseDetector(hyper_parameters)
