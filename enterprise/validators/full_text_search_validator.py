"""full_text_search validators."""

def validate_full_text_search(data: dict) -> list[str]:
    errors = []
    if not data:
        errors.append("full_text_search data is required")
    return errors
