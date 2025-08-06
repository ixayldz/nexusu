import hashlib
import json
from typing import Any, Optional

import redis.asyncio as redis
from app.core.settings import get_settings

_settings = get_settings()


def _hash(payload: dict[str, Any]) -> str:
    blob = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(blob.encode()).hexdigest()


async def get(namespace: str, payload: dict[str, Any]) -> Optional[str]:
    key = f"{namespace}:{_hash(payload)}"
    async with redis.from_url(
        _settings.redis_url, decode_responses=True
    ) as client:
        return await client.get(key)


async def set(
    namespace: str,
    payload: dict[str, Any],
    value: str,
    ttl: int = 3600,
) -> None:
    key = f"{namespace}:{_hash(payload)}"
    async with redis.from_url(
        _settings.redis_url, decode_responses=True
    ) as client:
        await client.set(key, value, ex=ttl)
