"""push validators."""

def validate_push(data: dict) -> list[str]:
    errors = []
    if not data:
        errors.append("push data is required")
    return errors
