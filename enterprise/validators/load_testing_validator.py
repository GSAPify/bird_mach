"""load_testing validators."""

def validate_load_testing(data: dict) -> list[str]:
    errors = []
    if not data:
        errors.append("load_testing data is required")
    return errors
