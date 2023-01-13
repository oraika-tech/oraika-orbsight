from typing import Any, Dict, Optional, Mapping, Union

from pydantic import BaseSettings, PrivateAttr
from pydantic import Field
from redis import Redis

from service.common.settings import settings


class EntityRedisManager(BaseSettings):
    host: str = Field("localhost", env='REDIS_HOST')
    port: int = Field(6379, env='REDIS_PORT')
    _key_prefix: str = PrivateAttr()
    _delimiter: str = PrivateAttr()
    _client: Redis = PrivateAttr()

    def __init__(self, key_prefix: str, **values: Any):
        super().__init__(**values)
        self._key_prefix = key_prefix + ":"
        self._delimiter = ","
        self._client = Redis(host=self.host, port=self.port, decode_responses=True)

    def _get_key(self, entity_id):
        return self._key_prefix + entity_id

    def _set_expiry(self, entity_key: str, expiry_at: Optional[int] = None, ttl: Optional[int] = None):
        if ttl:
            self._client.expire(entity_key, ttl)
        elif expiry_at:
            self._client.expireat(entity_key, expiry_at)
        else:
            self._client.expire(entity_key, settings.DEFAULT_MAX_CACHE_TTL_SECONDS)

    def set_value(self, key: str, value: str, expiry_at: Optional[int] = None, ttl: Optional[int] = None):
        self._client.set(key, value)
        self._set_expiry(key, expiry_at=expiry_at, ttl=ttl)

    def get_value(self, key: str) -> str:
        return str(self._client.get(key))

    def set_entity(self, entity_id: str, entity: Dict[str, str],
                   expiry_at: Optional[int] = None, ttl: Optional[int] = None):
        entity_map: Mapping[Union[str, bytes], Union[str, bytes]] = {
            key: value
            for key, value in entity.items()
            if value
        }
        entity_key = self._get_key(entity_id)
        self._client.hset(entity_key, mapping=entity_map)
        self._set_expiry(entity_key, expiry_at=expiry_at, ttl=ttl)

    def get_entity(self, entity_id: str):
        value = self._client.hgetall(self._get_key(entity_id))
        if value:
            value['ttl'] = self._client.ttl(entity_id)
        return value

    def update_entity(self, entity_id: str, field: str, value: Any):
        self._client.hset(self._get_key(entity_id), field, value)

    def delete_entity(self, entity_id: str):
        self._client.delete(self._get_key(entity_id))
