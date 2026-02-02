"""distributed_cache validators."""

def validate_distributed_cache(data: dict) -> list[str]:
    errors = []
    if not data:
        errors.append("distributed_cache data is required")
    return errors
