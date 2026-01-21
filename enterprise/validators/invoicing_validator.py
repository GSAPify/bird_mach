"""invoicing validators."""

def validate_invoicing(data: dict) -> list[str]:
    errors = []
    if not data:
        errors.append("invoicing data is required")
    return errors
