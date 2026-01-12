import random

from functools import lru_cache
from time import time
from typing import Annotated
from redis.asyncio import Redis
from fastapi import HTTPException, status, Request, Depends

from app.common.redis_api import get_redis


class RateLimiter:
    def __init__(self, redis: Redis):
        self._redis = redis
        self._lua_sha = None

    async def _load_script(self):
        if self._lua_sha is None:
            script = """
            redis.call("ZREMRANGEBYSCORE", KEYS[1], 0, ARGV[2])
            local count = redis.call("ZCARD", KEYS[1])
            if count >= tonumber(ARGV[3]) then
                return 1
            end
            redis.call("ZADD", KEYS[1], ARGV[1], ARGV[5])
            redis.call("EXPIRE", KEYS[1], ARGV[4])
            return 0
            """
            self._lua_sha = await self._redis.script_load(script)

    async def is_limited(
            self,
            ip_address: str,
            endpoint: str,
            max_requests: int,
            window_seconds: int,
    ) -> bool:
        key = f"rate_limiter:{endpoint}:{ip_address}"

        current_ms = time() * 1000
        window_start_ms = current_ms - window_seconds * 1000

        current_request = f"{current_ms}-{random.randint(0, 100_000)}"

        async with self._redis.pipeline() as pipe:
            await pipe.zremrangebyscore(key, 0, window_start_ms)

            await pipe.zcard(key)

            await pipe.zadd(key, {current_request: current_ms})

            await pipe.expire(key, window_seconds)

            res = await pipe.execute()

        _, current_count, _, _ = res
        return current_count >= max_requests

    async def is_limited_atomically(
            self,
            ip_address: str,
            endpoint: str,
            max_requests: int,
            window_seconds: int,
    ) -> bool:
        await self._load_script()

        key = f"rate_limiter:{endpoint}:{ip_address}"

        current_ms = int(time() * 1000)
        window_start_ms = current_ms - window_seconds * 1000
        member_id = f"{current_ms}-{random.randint(0, 100_000)}"

        result = await self._redis.evalsha(
            self._lua_sha,
            1,
            key,
            current_ms,
            window_start_ms,
            max_requests,
            window_seconds,
            member_id,
        )

        return result == 1


@lru_cache
def get_rate_limiter() -> RateLimiter:
    return RateLimiter(get_redis())


def rate_limiter_factory(
        endpoint: str,
        max_requests: int,
        window_seconds: int,
):
    async def dependency(
            request: Request,
            rate_limiter: Annotated[RateLimiter, Depends(get_rate_limiter)],
    ):
        ip_address = request.client.host

        limited = await rate_limiter.is_limited_atomically(
            ip_address,
            endpoint,
            max_requests,
            window_seconds,
        )

        if limited:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Too many requests. Please try again later"
            )

    return dependency


"""
To use Rate Limiter on endpoint past 'dependencies=[Depends(rate_limit_protected_page)]'

eg.:
rate_limit_protected_page = rate_limiter_factory("protected_page", 5, 5)
app.get("/protected_page", dependencies=[Depends(rate_limit_protected_page)])
"""
