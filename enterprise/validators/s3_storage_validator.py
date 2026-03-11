"""s3_storage validators."""

def validate_s3_storage(data: dict) -> list[str]:
    errors = []
    if not data:
        errors.append("s3_storage data is required")
    return errors
