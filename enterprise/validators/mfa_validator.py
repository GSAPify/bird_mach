"""mfa validators."""

def validate_mfa(data: dict) -> list[str]:
    errors = []
    if not data:
        errors.append("mfa data is required")
    return errors
