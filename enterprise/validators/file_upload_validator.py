"""file_upload validators."""

def validate_file_upload(data: dict) -> list[str]:
    errors = []
    if not data:
        errors.append("file_upload data is required")
    return errors
