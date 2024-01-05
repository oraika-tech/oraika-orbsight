import json
import logging
from dataclasses import dataclass, asdict
from typing import Optional

import requests
from pydantic import BaseModel

from service.common.config.app_settings import app_settings

spacepulse_url = app_settings.SPACEPULSE_URL
spacepulse_api_key = app_settings.SPACEPULSE_API_KEY
spacepulse_api_secret = app_settings.SPACEPULSE_API_SECRET

logger = logging.getLogger(__name__)


class SpacePulseTenantInfo(BaseModel):
    tenant_code: str
    partner_id: int


@dataclass
class SpacePulsePostRequest:
    id: int
    text: str
    source: str
    sentiment: str
    departments: list[str]
    activities: list[str]
    people: list[str]
    timestamp: int
    link: Optional[str] = None
    rating: Optional[int] = None
    owner_answer_timestamp: Optional[int] = None
    likes: Optional[int] = None

    def to_json(self):
        return json.dumps(asdict(self))


def spacepulse_post(tenant_info: SpacePulseTenantInfo, review_data: SpacePulsePostRequest):
    response = requests.post(
        spacepulse_url,
        headers={
            'tenant': tenant_info.tenant_code,
            'Content-Type': 'application/json',
            'xapikey': spacepulse_api_key,
            'xapisecret': spacepulse_api_secret
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
