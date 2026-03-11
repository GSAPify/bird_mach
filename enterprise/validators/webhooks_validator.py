"""webhooks validators."""

def validate_webhooks(data: dict) -> list[str]:
    errors = []
    if not data:
        errors.append("webhooks data is required")
    return errors
