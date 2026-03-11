"""timezone validators."""

def validate_timezone(data: dict) -> list[str]:
    errors = []
    if not data:
        errors.append("timezone data is required")
    return errors
