"""sms validators."""

def validate_sms(data: dict) -> list[str]:
    errors = []
    if not data:
        errors.append("sms data is required")
    return errors
