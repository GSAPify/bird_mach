"""scheduling validators."""

def validate_scheduling(data: dict) -> list[str]:
    errors = []
    if not data:
        errors.append("scheduling data is required")
    return errors
