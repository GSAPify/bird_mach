"""video_thumb validators."""

def validate_video_thumb(data: dict) -> list[str]:
    errors = []
    if not data:
        errors.append("video_thumb data is required")
    return errors
