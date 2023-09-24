from typing import List, Any, Dict

import requests
from pydantic import BaseSettings, Field, PrivateAttr
from requests import Timeout

GRAFANA_API_ENDPOINT = "https://grafana.oraika.com/api/alertmanager/grafana/api/v2/alerts"


class GrafanaClient(BaseSettings):
    _headers: Dict[str, Any] = PrivateAttr()
    endpoint: str = GRAFANA_API_ENDPOINT
    api_key: str = Field('eyJrIjoiSXpzVzFXdjdQWElYcFNGYmlyVVdhYmZGNGppRldvUFoiLCJuIjoidmlld2VyX2FjY2VzcyIsImlkIjoxfQ==',
                         env="GRAFANA_API_KEY")

    previous_value: List[Dict[str, Any]] = []

    def __init__(self, **data: Any):
        super().__init__(**data)

        self._headers = {
            "accept": "*/*",
            "content-type": "application/json",
            "authorization": "Bearer {}".format(self.api_key)
        }

    def get_alerts(self) -> List[Dict[str, Any]]:

        try:
            response = requests.request("GET", self.endpoint, headers=self._headers, timeout=5)

            if response.status_code == 200:
                alerts = response.json()
                self.previous_value = alerts
                return alerts

            raise RuntimeError(f"Grafana Get API Error: {response.text}")

        except Timeout as ex:
            return self.previous_value

        except Exception as ex:
            raise RuntimeError(f"Grafana Get API Exception: {ex}")
