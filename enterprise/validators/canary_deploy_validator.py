"""canary_deploy validators."""

def validate_canary_deploy(data: dict) -> list[str]:
    errors = []
    if not data:
        errors.append("canary_deploy data is required")
    return errors
