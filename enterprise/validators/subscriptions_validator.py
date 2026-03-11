"""subscriptions validators."""

def validate_subscriptions(data: dict) -> list[str]:
    errors = []
    if not data:
        errors.append("subscriptions data is required")
    return errors
