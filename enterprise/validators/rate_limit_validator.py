"""rate_limit validators."""

def validate_rate_limit(data: dict) -> list[str]:
    errors = []
    if not data:
        errors.append("rate_limit data is required")
    return errors
