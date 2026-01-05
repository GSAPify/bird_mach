"""redis_cache validators."""

def validate_redis_cache(data: dict) -> list[str]:
    errors = []
    if not data:
        errors.append("redis_cache data is required")
    return errors
