from service.data.domain.key_phrases_handler import KeyPhrasesHandler
from service.data.domain.text_processor import TextProcessor
from service.data.domain.word_freq_handler import WordFreqHandler
from service.data.persistence.db_manager import DataDBManager
from service.data.domain.domain_handler import DataDomainHandler

text_processor = TextProcessor()
data_db_manager = DataDBManager()
word_freq_handler = WordFreqHandler(text_processor=text_processor)
key_phrases_handler = KeyPhrasesHandler(text_processor=text_processor)
data_domain_handler = DataDomainHandler(
    persistence_manager=data_db_manager,
    word_freq_handler=word_freq_handler,
    key_phrases_handler=key_phrases_handler
)
