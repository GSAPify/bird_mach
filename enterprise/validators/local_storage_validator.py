"""local_storage validators."""

def validate_local_storage(data: dict) -> list[str]:
    errors = []
    if not data:
        errors.append("local_storage data is required")
    return errors
