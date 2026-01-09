"""email validators."""

def validate_email(data: dict) -> list[str]:
    errors = []
    if not data:
        errors.append("email data is required")
    return errors
