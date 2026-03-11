"""metrics validators."""

def validate_metrics(data: dict) -> list[str]:
    errors = []
    if not data:
        errors.append("metrics data is required")
    return errors
