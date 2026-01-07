"""runbooks validators."""

def validate_runbooks(data: dict) -> list[str]:
    errors = []
    if not data:
        errors.append("runbooks data is required")
    return errors
