"""elasticsearch validators."""

def validate_elasticsearch(data: dict) -> list[str]:
    errors = []
    if not data:
        errors.append("elasticsearch data is required")
    return errors
