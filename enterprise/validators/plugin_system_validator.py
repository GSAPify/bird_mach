"""plugin_system validators."""

def validate_plugin_system(data: dict) -> list[str]:
    errors = []
    if not data:
        errors.append("plugin_system data is required")
    return errors
