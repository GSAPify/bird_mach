"""usage_metering validators."""

def validate_usage_metering(data: dict) -> list[str]:
    errors = []
    if not data:
        errors.append("usage_metering data is required")
    return errors
