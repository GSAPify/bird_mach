"""user_preferences validators."""

def validate_user_preferences(data: dict) -> list[str]:
    errors = []
    if not data:
        errors.append("user_preferences data is required")
    return errors
