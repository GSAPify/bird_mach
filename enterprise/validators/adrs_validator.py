"""adrs validators."""

def validate_adrs(data: dict) -> list[str]:
    errors = []
    if not data:
        errors.append("adrs data is required")
    return errors
