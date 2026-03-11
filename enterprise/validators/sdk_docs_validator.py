"""sdk_docs validators."""

def validate_sdk_docs(data: dict) -> list[str]:
    errors = []
    if not data:
        errors.append("sdk_docs data is required")
    return errors
