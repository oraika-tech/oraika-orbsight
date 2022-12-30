from typing import List, Dict

from pydantic import BaseSettings

from .model.key_phrase import KeyPhraseWeight, EmotionKeyPhrases
from .model.text_analysis_data import TextAnalysisData
from .text_processor import TextProcessor


class KeyPhrasesHandler(BaseSettings):
    text_processor: TextProcessor

    @staticmethod
    def get_distance(el):
        return el.distance

    def generate_key_phrases(self, data: List[TextAnalysisData], lang_code: str):
        if not data or len(data) == 0:
            return

        emotion_text_map: Dict[str, List[str]] = {}
        for text_analysis_data in data:
            if text_analysis_data.emotion is None:
                continue
            if text_analysis_data.emotion not in emotion_text_map:
                emotion_text_map[text_analysis_data.emotion] = []
            emotion_text_map[text_analysis_data.emotion].append(text_analysis_data.raw_text)

        response: List[EmotionKeyPhrases] = []
        for key, value in emotion_text_map.items():
            text = "\n".join(value)
            cleaned_text = self.text_processor.clean_text(text)
            extracted_phrases = self.text_processor.extract_key_phrases(
                text=cleaned_text,
                lang_code=lang_code,
                remove_stopwords=False,
            )

            key_phrases = [
                KeyPhraseWeight(phrase=key_phrase, distance=distance)
                for key_phrase, distance in extracted_phrases.items()
            ]
            key_phrases.sort(key=self.get_distance, reverse=True)

            response.append(
                EmotionKeyPhrases(
                    name=key,
                    key_phrases=key_phrases
                )
            )

        return response
