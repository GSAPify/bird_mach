"""oauth2 validators."""

def validate_oauth2(data: dict) -> list[str]:
    errors = []
    if not data:
        errors.append("oauth2 data is required")
    return errors
