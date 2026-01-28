"""Test fixtures for shares."""
    import uuid
    from datetime import datetime

    def make_share(**overrides):
        defaults = {
            "id": str(uuid.uuid4()),
            "created_at": datetime(2026, 1, 1),
            "updated_at": datetime(2026, 1, 1),
        }
        defaults.update(overrides)
        return defaults

    SAMPLE_SHARES = [make_share() for _ in range(5)]
