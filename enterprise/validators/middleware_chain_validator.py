"""middleware_chain validators."""

def validate_middleware_chain(data: dict) -> list[str]:
    errors = []
    if not data:
        errors.append("middleware_chain data is required")
    return errors
