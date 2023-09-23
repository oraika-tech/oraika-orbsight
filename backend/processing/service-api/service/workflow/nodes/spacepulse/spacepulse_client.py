import json
import logging
import os
from dataclasses import dataclass, asdict

import requests
from pydantic import BaseModel

spacepulse_url = os.environ["SPACEPULSE_URL"]
spacepulse_api_key = os.environ["SPACEPULSE_API_KEY"]

logger = logging.getLogger(__name__)


class SpacePulseTenantInfo(BaseModel):
    tenant_code: str
    partner_id: int


@dataclass
class SpacePulsePostRequest:
    id: int
    text: str
    source: str
    link: str
    sentiment: str
    departments: list[str]
    activities: list[str]
    rating: int
    timestamp: int
    owner_answer_timestamp: int
    likes: int

    # def to_str(self):
    #     return "\n".join(f"{key}: {value}" for key, value in asdict(self).items())

    def to_json(self):
        return json.dumps(asdict(self))


def spacepulse_post(tenant_info: SpacePulseTenantInfo, review_data: SpacePulsePostRequest):
    response = requests.post(
        spacepulse_url,
        headers={
            'tenant': tenant_info.tenant_code,
            'Content-Type': 'application/json',
            'Cookie': 'JSESSIONID=' + spacepulse_api_key
        },
        json={
            # "enquiryMessage": review_data.to_str(),
            "internalFields": review_data.to_json(),
            "consumerPhoneNumber": "7338677991",
            "partnerId": tenant_info.partner_id,
            "channel": "Oraika",
            "entityType": "Obsights",
            "type": "Obsights",
            "isDraft": 1,
            "version": "2"
        })
    logger.info("response=%s", response)
    return response
