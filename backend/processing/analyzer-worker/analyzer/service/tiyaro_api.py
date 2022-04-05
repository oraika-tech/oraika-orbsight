from typing import Optional, List, Any, Dict

import requests
from pydantic import BaseSettings, Field, PrivateAttr

from analyzer.api.tiyaro_exception import TiyaroException

TIYARO_API_ENDPOINT = "https://api.tiyaro.ai/v1/ent/huggingface/1/{model}"
ZERO_SHOT_MODEL = "joeddav/xlm-roberta-large-xnli"
TRANSLATION_MODEL = "Helsinki-NLP/opus-mt-mul-en"


class TiyaroClient(BaseSettings):
    _headers: Dict[str, Any] = PrivateAttr()
    endpoint_format: Optional[str] = TIYARO_API_ENDPOINT
    api_key: str = Field(env="TIYARO_API_KEY")

    def __init__(self, **data: Any):
        super().__init__(**data)

        self._headers = {
            "accept": "*/*",
            "content-type": "application/json",
            "authorization": "Bearer {}".format(self.api_key)
        }

    def classify_text(self, text: str, labels: List[str], multi_label: Optional[bool] = True) -> Dict[str, float]:
        endpoint = self.endpoint_format.format(model=ZERO_SHOT_MODEL)

        payload = {
            "input": text,
            "multiLabel": multi_label,
            "labels": labels
        }

        try:
            response = requests.request("POST", endpoint, json=payload, headers=self._headers)

            if response.status_code == 200:
                json_response = response.json()
                return dict(zip(json_response["response"]["labels"], json_response["response"]["scores"]))

            raise TiyaroException(f"Tiyaro ZS API Error: {response.text}")
        except Exception as ex:
            raise TiyaroException(f"Tiyaro ZS API Exception: {ex}")

    def translate_text(self, text: str) -> str:
        endpoint = self.endpoint_format.format(model=TRANSLATION_MODEL)

        payload = {"input": text}

        try:
            response = requests.request("POST", endpoint, json=payload, headers=self._headers)
            if response.status_code == 200:
                json_response = response.json()
                if "response" in json_response and len(json_response["response"]) > 0:
                    return json_response["response"][0]["translation_text"]

            raise TiyaroException(f"Tiyaro Translate API Error: {response.text}")
        except Exception as ex:
            raise TiyaroException(f"Tiyaro Translate API Exception: {ex}")
