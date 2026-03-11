"""search validators."""

def validate_search(data: dict) -> list[str]:
    errors = []
    if not data:
        errors.append("search data is required")
    return errors
