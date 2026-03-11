"""in_memory_cache validators."""

def validate_in_memory_cache(data: dict) -> list[str]:
    errors = []
    if not data:
        errors.append("in_memory_cache data is required")
    return errors
