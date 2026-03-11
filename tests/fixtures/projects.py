"""Test fixtures for projects."""
    import uuid
    from datetime import datetime

    def make_project(**overrides):
        defaults = {
            "id": str(uuid.uuid4()),
            "created_at": datetime(2026, 1, 1),
            "updated_at": datetime(2026, 1, 1),
        }
        defaults.update(overrides)
        return defaults

    SAMPLE_PROJECTS = [make_project() for _ in range(5)]
