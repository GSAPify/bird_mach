"""audit_log validators."""

def validate_audit_log(data: dict) -> list[str]:
    errors = []
    if not data:
        errors.append("audit_log data is required")
    return errors
