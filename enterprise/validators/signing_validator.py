"""signing validators."""

def validate_signing(data: dict) -> list[str]:
    errors = []
    if not data:
        errors.append("signing data is required")
    return errors
