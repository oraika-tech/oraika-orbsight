from typing import Optional, List

from pydantic import BaseModel


class KeyPhraseWeight(BaseModel):
    phrase: str
    distance: Optional[float]


class EmotionKeyPhrases(BaseModel):
    name: str
    polarity: Optional[int]
    key_phrases: List[KeyPhraseWeight]