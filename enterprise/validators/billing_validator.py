"""billing validators."""

def validate_billing(data: dict) -> list[str]:
    errors = []
    if not data:
        errors.append("billing data is required")
    return errors
