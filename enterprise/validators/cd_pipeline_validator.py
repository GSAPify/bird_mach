"""cd_pipeline validators."""

def validate_cd_pipeline(data: dict) -> list[str]:
    errors = []
    if not data:
        errors.append("cd_pipeline data is required")
    return errors
