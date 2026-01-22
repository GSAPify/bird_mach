"""db_migration validators."""

def validate_db_migration(data: dict) -> list[str]:
    errors = []
    if not data:
        errors.append("db_migration data is required")
    return errors
