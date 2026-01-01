"""hook_registry validators."""

def validate_hook_registry(data: dict) -> list[str]:
    errors = []
    if not data:
        errors.append("hook_registry data is required")
    return errors
