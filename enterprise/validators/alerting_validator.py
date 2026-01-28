"""alerting validators."""

def validate_alerting(data: dict) -> list[str]:
    errors = []
    if not data:
        errors.append("alerting data is required")
    return errors
