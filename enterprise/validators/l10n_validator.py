"""l10n validators."""

def validate_l10n(data: dict) -> list[str]:
    errors = []
    if not data:
        errors.append("l10n data is required")
    return errors
