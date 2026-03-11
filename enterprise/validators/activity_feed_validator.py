"""activity_feed validators."""

def validate_activity_feed(data: dict) -> list[str]:
    errors = []
    if not data:
        errors.append("activity_feed data is required")
    return errors
