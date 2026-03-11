"""model_registry validators."""

def validate_model_registry(data: dict) -> list[str]:
    errors = []
    if not data:
        errors.append("model_registry data is required")
    return errors
