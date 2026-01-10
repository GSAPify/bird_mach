"""connection_pool validators."""

def validate_connection_pool(data: dict) -> list[str]:
    errors = []
    if not data:
        errors.append("connection_pool data is required")
    return errors
