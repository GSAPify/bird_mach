"""dashboard validators."""

def validate_dashboard(data: dict) -> list[str]:
    errors = []
    if not data:
        errors.append("dashboard data is required")
    return errors
