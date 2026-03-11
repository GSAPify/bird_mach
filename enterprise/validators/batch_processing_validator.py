"""batch_processing validators."""

def validate_batch_processing(data: dict) -> list[str]:
    errors = []
    if not data:
        errors.append("batch_processing data is required")
    return errors
