"""team_mgmt validators."""

def validate_team_mgmt(data: dict) -> list[str]:
    errors = []
    if not data:
        errors.append("team_mgmt data is required")
    return errors
