from typing import List, Dict

from pydantic import BaseSettings, Field

from .model.text_analysis_data import TextAnalysisData
from .model.word_freq import EmotionWordFrequency, TextWordWeight
from .text_processor import TextProcessor


class WordFreqHandler(BaseSettings):
    minimum_frequency: int = Field(2, env='MINIMUM_FREQUENCY')
    text_processor: TextProcessor

    def generate_word_freq(self, data: List[TextAnalysisData], lang_code: str):
        if not data or len(data) == 0:
            return

        emotion_text_map: Dict[str, List[str]] = {}
        for text_analysis_data in data:
            if text_analysis_data.emotion not in emotion_text_map:
                emotion_text_map[text_analysis_data.emotion] = []
            emotion_text_map[text_analysis_data.emotion].append(text_analysis_data.raw_text)

        emotion_str_map: Dict[str, str] = {}
        for key, value in emotion_text_map.items():
            text = "".join(value)
            cleaned_text = self.text_processor.clean_text(text)

            emotion_str_map[key] = cleaned_text.lower()

        # Create and generate a word cloud image:
        response: List[EmotionWordFrequency] = []
        for key, value in emotion_str_map.items():
            response.append(
                EmotionWordFrequency(
                    name=key,
                    word_cloud=[
                        TextWordWeight(term=word, weight=frequency)
                        for word, frequency in self.generate_freq_map(lang_code=lang_code, text=value).items()
                        if frequency > self.minimum_frequency
                    ]
                )
            )

        return response

    def generate_freq_map(self, lang_code: str, text: str) -> Dict[str, int]:
        frequency_count: Dict[str, int] = {}
        word_list = text.split()
        for word in word_list:
            cleaned_text = self.text_processor.clean_text(text=word, deep_clean=True, lang_code=lang_code)
            if cleaned_text.strip() != "":
                if word in frequency_count:
                    frequency_count[word] += 1
                else:
                    frequency_count[word] = 1

        return frequency_count
