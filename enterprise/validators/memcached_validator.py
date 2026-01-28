"""memcached validators."""

def validate_memcached(data: dict) -> list[str]:
    errors = []
    if not data:
        errors.append("memcached data is required")
    return errors
