"""integration_testing validators."""

def validate_integration_testing(data: dict) -> list[str]:
    errors = []
    if not data:
        errors.append("integration_testing data is required")
    return errors
