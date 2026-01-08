"""locale validators."""

def validate_locale(data: dict) -> list[str]:
    errors = []
    if not data:
        errors.append("locale data is required")
    return errors
