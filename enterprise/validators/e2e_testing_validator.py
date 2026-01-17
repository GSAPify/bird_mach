"""e2e_testing validators."""

def validate_e2e_testing(data: dict) -> list[str]:
    errors = []
    if not data:
        errors.append("e2e_testing data is required")
    return errors
