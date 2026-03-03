"""fuzzy_match validators."""

def validate_fuzzy_match(data: dict) -> list[str]:
    errors = []
    if not data:
        errors.append("fuzzy_match data is required")
    return errors
