"""long_polling validators."""

def validate_long_polling(data: dict) -> list[str]:
    errors = []
    if not data:
        errors.append("long_polling data is required")
    return errors
