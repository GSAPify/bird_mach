"""db_seeding validators."""

def validate_db_seeding(data: dict) -> list[str]:
    errors = []
    if not data:
        errors.append("db_seeding data is required")
    return errors
