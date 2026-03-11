"""pagination validators."""

def validate_pagination(data: dict) -> list[str]:
    errors = []
    if not data:
        errors.append("pagination data is required")
    return errors
