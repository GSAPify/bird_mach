"""filtering validators."""

def validate_filtering(data: dict) -> list[str]:
    errors = []
    if not data:
        errors.append("filtering data is required")
    return errors
