"""currency validators."""

def validate_currency(data: dict) -> list[str]:
    errors = []
    if not data:
        errors.append("currency data is required")
    return errors
