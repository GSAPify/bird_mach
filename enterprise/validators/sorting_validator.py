"""sorting validators."""

def validate_sorting(data: dict) -> list[str]:
    errors = []
    if not data:
        errors.append("sorting data is required")
    return errors
