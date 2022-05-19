from typing import Optional, List

from pydantic import BaseModel


class TextWordWeight(BaseModel):
    term: str
    weight: int


class EmotionWordFrequency(BaseModel):
    name: str
    polarity: Optional[int]
    word_cloud: List[TextWordWeight]
