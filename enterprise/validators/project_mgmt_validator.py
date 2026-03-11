"""project_mgmt validators."""

def validate_project_mgmt(data: dict) -> list[str]:
    errors = []
    if not data:
        errors.append("project_mgmt data is required")
    return errors
