"""api_keys validators."""

def validate_api_keys(data: dict) -> list[str]:
    errors = []
    if not data:
        errors.append("api_keys data is required")
    return errors
