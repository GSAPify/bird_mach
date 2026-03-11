"""azure_blob validators."""

def validate_azure_blob(data: dict) -> list[str]:
    errors = []
    if not data:
        errors.append("azure_blob data is required")
    return errors
