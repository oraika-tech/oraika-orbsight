from typing import List, Dict, Optional

from pydantic import BaseModel

from service.app.data.data_models import TextAnalysisData
from service.app.data.utils.text_processor import clean_text, extract_key_phrases


class KeyPhraseWeight(BaseModel):
    phrase: str
    distance: Optional[float] = None


class EmotionKeyPhrases(BaseModel):
    name: str
    polarity: Optional[int] = None
    key_phrases: List[KeyPhraseWeight]


def get_distance(el):
    return el.distance


def generate_key_phrases(data: List[TextAnalysisData]):
    if not data or len(data) == 0:
        return

    emotion_text_map: Dict[str, List[str]] = {}
    for text_analysis_data in data:
        if not text_analysis_data.emotion:
            continue
        if text_analysis_data.emotion not in emotion_text_map:
            emotion_text_map[text_analysis_data.emotion] = []
        emotion_text_map[text_analysis_data.emotion].append(text_analysis_data.raw_text)

    response: List[EmotionKeyPhrases] = []
    for key, value in emotion_text_map.items():
        text = "\n".join(value)
        cleaned_text = clean_text(text)
        extracted_phrases = extract_key_phrases(cleaned_text)

        key_phrases = [
            KeyPhraseWeight(phrase=key_phrase, distance=distance)
            for key_phrase, distance in extracted_phrases.items()
        ]
        key_phrases.sort(key=get_distance, reverse=True)

        response.append(
            EmotionKeyPhrases(
                name=key,
                key_phrases=key_phrases
            )
        )

    return response
