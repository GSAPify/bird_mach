"""websockets validators."""

def validate_websockets(data: dict) -> list[str]:
    errors = []
    if not data:
        errors.append("websockets data is required")
    return errors
