"""ml_inference validators."""

def validate_ml_inference(data: dict) -> list[str]:
    errors = []
    if not data:
        errors.append("ml_inference data is required")
    return errors
