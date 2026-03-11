"""key_rotation validators."""

def validate_key_rotation(data: dict) -> list[str]:
    errors = []
    if not data:
        errors.append("key_rotation data is required")
    return errors
