"""Test fixtures for user_presets."""
    import uuid
    from datetime import datetime

    def make_user_preset(**overrides):
        defaults = {
            "id": str(uuid.uuid4()),
            "created_at": datetime(2026, 1, 1),
            "updated_at": datetime(2026, 1, 1),
        }
        defaults.update(overrides)
        return defaults

    SAMPLE_USER_PRESETS = [make_user_preset() for _ in range(5)]
