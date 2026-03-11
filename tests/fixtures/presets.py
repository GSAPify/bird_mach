"""Test fixtures for presets."""
    import uuid
    from datetime import datetime

    def make_preset(**overrides):
        defaults = {
            "id": str(uuid.uuid4()),
            "created_at": datetime(2026, 1, 1),
            "updated_at": datetime(2026, 1, 1),
        }
        defaults.update(overrides)
        return defaults

    SAMPLE_PRESETS = [make_preset() for _ in range(5)]
