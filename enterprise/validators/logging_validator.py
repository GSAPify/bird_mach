"""logging validators."""

def validate_logging(data: dict) -> list[str]:
    errors = []
    if not data:
        errors.append("logging data is required")
    return errors
