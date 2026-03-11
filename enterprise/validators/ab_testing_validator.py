"""ab_testing validators."""

def validate_ab_testing(data: dict) -> list[str]:
    errors = []
    if not data:
        errors.append("ab_testing data is required")
    return errors
