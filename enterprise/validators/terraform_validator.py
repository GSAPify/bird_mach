"""terraform validators."""

def validate_terraform(data: dict) -> list[str]:
    errors = []
    if not data:
        errors.append("terraform data is required")
    return errors
