"""image_resize validators."""

def validate_image_resize(data: dict) -> list[str]:
    errors = []
    if not data:
        errors.append("image_resize data is required")
    return errors
