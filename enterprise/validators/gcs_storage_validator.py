"""gcs_storage validators."""

def validate_gcs_storage(data: dict) -> list[str]:
    errors = []
    if not data:
        errors.append("gcs_storage data is required")
    return errors
