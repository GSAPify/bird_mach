"""db_backup validators."""

def validate_db_backup(data: dict) -> list[str]:
    errors = []
    if not data:
        errors.append("db_backup data is required")
    return errors
