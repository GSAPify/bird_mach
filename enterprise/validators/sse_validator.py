"""sse validators."""

def validate_sse(data: dict) -> list[str]:
    errors = []
    if not data:
        errors.append("sse data is required")
    return errors
