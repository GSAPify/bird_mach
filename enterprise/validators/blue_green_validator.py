"""blue_green validators."""

def validate_blue_green(data: dict) -> list[str]:
    errors = []
    if not data:
        errors.append("blue_green data is required")
    return errors
