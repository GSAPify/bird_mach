"""real_time validators."""

def validate_real_time(data: dict) -> list[str]:
    errors = []
    if not data:
        errors.append("real_time data is required")
    return errors
