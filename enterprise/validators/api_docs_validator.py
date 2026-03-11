"""api_docs validators."""

def validate_api_docs(data: dict) -> list[str]:
    errors = []
    if not data:
        errors.append("api_docs data is required")
    return errors
