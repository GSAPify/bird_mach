"""helm_charts validators."""

def validate_helm_charts(data: dict) -> list[str]:
    errors = []
    if not data:
        errors.append("helm_charts data is required")
    return errors
