"""audio_transcode validators."""

def validate_audio_transcode(data: dict) -> list[str]:
    errors = []
    if not data:
        errors.append("audio_transcode data is required")
    return errors
