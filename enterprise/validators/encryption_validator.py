"""encryption validators."""

def validate_encryption(data: dict) -> list[str]:
    errors = []
    if not data:
        errors.append("encryption data is required")
    return errors
