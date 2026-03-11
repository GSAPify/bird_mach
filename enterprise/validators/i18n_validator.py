"""i18n validators."""

def validate_i18n(data: dict) -> list[str]:
    errors = []
    if not data:
        errors.append("i18n data is required")
    return errors
