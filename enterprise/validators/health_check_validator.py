"""health_check validators."""

def validate_health_check(data: dict) -> list[str]:
    errors = []
    if not data:
        errors.append("health_check data is required")
    return errors
