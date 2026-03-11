"""unit_testing validators."""

def validate_unit_testing(data: dict) -> list[str]:
    errors = []
    if not data:
        errors.append("unit_testing data is required")
    return errors
