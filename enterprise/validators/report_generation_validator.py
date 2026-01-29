"""report_generation validators."""

def validate_report_generation(data: dict) -> list[str]:
    errors = []
    if not data:
        errors.append("report_generation data is required")
    return errors
