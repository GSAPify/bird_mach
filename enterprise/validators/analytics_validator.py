"""analytics validators."""

def validate_analytics(data: dict) -> list[str]:
    errors = []
    if not data:
        errors.append("analytics data is required")
    return errors
