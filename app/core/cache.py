import hashlib
import json
from typing import Any, Optional

import redis.asyncio as redis
from redis.exceptions import RedisError

from app.core.settings import get_settings

_settings = get_settings()


def _hash(payload: dict[str, Any]) -> str:
    blob = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(blob.encode()).hexdigest()


async def get(namespace: str, payload: dict[str, Any]) -> Optional[str]:
    """Fetch a cached value.

    If the Redis server is unavailable the cache is simply bypassed. This keeps
    the application functional in development and test environments where a
    backing Redis instance may not exist.
    """

    key = f"{namespace}:{_hash(payload)}"
    try:
        async with redis.from_url(
            _settings.redis_url, decode_responses=True
        ) as client:
            return await client.get(key)
    except RedisError:
        return None


async def set(
    namespace: str,
    payload: dict[str, Any],
    value: str,
    ttl: int = 3600,
) -> None:
    """Store a value in the cache.

    Failures to reach Redis are ignored so callers need not handle these
    scenarios explicitly.
    """

    key = f"{namespace}:{_hash(payload)}"
    try:
        async with redis.from_url(
            _settings.redis_url, decode_responses=True
        ) as client:
            await client.set(key, value, ex=ttl)
    except RedisError:
        pass
