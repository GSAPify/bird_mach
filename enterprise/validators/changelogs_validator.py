"""changelogs validators."""

def validate_changelogs(data: dict) -> list[str]:
    errors = []
    if not data:
        errors.append("changelogs data is required")
    return errors
