"""hashing validators."""

def validate_hashing(data: dict) -> list[str]:
    errors = []
    if not data:
        errors.append("hashing data is required")
    return errors
