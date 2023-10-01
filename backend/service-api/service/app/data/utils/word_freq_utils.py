from typing import List, Dict, Tuple, Optional

from pydantic import BaseModel

from service.app.data.data_models import TextAnalysisData
from service.app.data.utils.text_processor import clean_text
from service.common.config.app_settings import app_settings


def generate_word_freq(data: List[TextAnalysisData], lang_code: str):
    if not data or len(data) == 0:
        return

    emotion_text_map: Dict[str, List[str]] = {}
    for text_analysis_data in data:
        if not text_analysis_data.emotion:
            continue
        if text_analysis_data.emotion not in emotion_text_map:
            emotion_text_map[text_analysis_data.emotion] = []
        emotion_text_map[text_analysis_data.emotion].append(text_analysis_data.raw_text)

    emotion_str_map: Dict[str, str] = {}
    for emotion, text_list in emotion_text_map.items():
        text = " ".join(text_list)
        cleaned_text = clean_text(text)

        emotion_str_map[emotion] = cleaned_text.lower()

    # Create and generate a word cloud image:
    response: List[EmotionWordFrequency] = []
    for emotion, cleaned_text in emotion_str_map.items():
        response.append(
            EmotionWordFrequency(
                name=emotion,
                word_cloud=[
                               TextWordWeight(term=word, weight=frequency)
                               for word, frequency in generate_freq_map(lang_code=lang_code, text=cleaned_text)
                           ][:app_settings.MAX_WORD_COUNT]
            )
        )

    return response


def generate_freq_map(lang_code: str, text: str) -> List[Tuple[str, int]]:
    frequency_count: Dict[str, int] = {}
    word_list = text.split()
    for word in word_list:
        cleaned_text = clean_text(text=word, deep_clean=True, lang_code=lang_code)
        if cleaned_text.strip() != "":
            if word in frequency_count:
                frequency_count[word] += 1
            else:
                frequency_count[word] = 1

    return sorted(frequency_count.items(), key=lambda item: item[1], reverse=True)


class TextWordWeight(BaseModel):
    term: str
    weight: int


class EmotionWordFrequency(BaseModel):
    name: str
    polarity: Optional[int]
    word_cloud: List[TextWordWeight]
