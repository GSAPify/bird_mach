"""feature_store validators."""

def validate_feature_store(data: dict) -> list[str]:
    errors = []
    if not data:
        errors.append("feature_store data is required")
    return errors
