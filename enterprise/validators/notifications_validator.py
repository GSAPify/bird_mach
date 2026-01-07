"""notifications validators."""

def validate_notifications(data: dict) -> list[str]:
    errors = []
    if not data:
        errors.append("notifications data is required")
    return errors
