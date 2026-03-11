"""Test fixtures for audio_tags."""
    import uuid
    from datetime import datetime

    def make_audio_tag(**overrides):
        defaults = {
            "id": str(uuid.uuid4()),
            "created_at": datetime(2026, 1, 1),
            "updated_at": datetime(2026, 1, 1),
        }
        defaults.update(overrides)
        return defaults

    SAMPLE_AUDIO_TAGS = [make_audio_tag() for _ in range(5)]
