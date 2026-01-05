"""event_bus validators."""

def validate_event_bus(data: dict) -> list[str]:
    errors = []
    if not data:
        errors.append("event_bus data is required")
    return errors
