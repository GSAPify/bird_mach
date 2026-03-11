"""ci_pipeline validators."""

def validate_ci_pipeline(data: dict) -> list[str]:
    errors = []
    if not data:
        errors.append("ci_pipeline data is required")
    return errors
