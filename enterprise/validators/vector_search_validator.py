"""vector_search validators."""

def validate_vector_search(data: dict) -> list[str]:
    errors = []
    if not data:
        errors.append("vector_search data is required")
    return errors
