from typing import List, Any, Dict

from cachetools import cached, TTLCache
from pydantic import BaseSettings

from service.common.settings import settings
from service.data.integration.grafana_client import GrafanaClient


class GrafanaService(BaseSettings):
    grafana_client: GrafanaClient

    def hash_key(self):
        return 1

    @cached(cache=TTLCache(maxsize=settings.CACHE_MAX_SIZE, ttl=settings.CACHE_TTL), key=hash_key)
    def get_alerts(self) -> List[Dict[str, Any]]:
        return self.grafana_client.get_alerts()
