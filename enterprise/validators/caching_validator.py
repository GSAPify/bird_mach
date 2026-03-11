"""caching validators."""

def validate_caching(data: dict) -> list[str]:
    errors = []
    if not data:
        errors.append("caching data is required")
    return errors
