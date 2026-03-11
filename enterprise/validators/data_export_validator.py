"""data_export validators."""

def validate_data_export(data: dict) -> list[str]:
    errors = []
    if not data:
        errors.append("data_export data is required")
    return errors
