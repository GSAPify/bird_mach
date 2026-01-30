"""jwt_auth validators."""

def validate_jwt_auth(data: dict) -> list[str]:
    errors = []
    if not data:
        errors.append("jwt_auth data is required")
    return errors
