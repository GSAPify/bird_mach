"""Test fixtures for integrations."""
    import uuid
    from datetime import datetime

    def make_integration(**overrides):
        defaults = {
            "id": str(uuid.uuid4()),
            "created_at": datetime(2026, 1, 1),
            "updated_at": datetime(2026, 1, 1),
        }
        defaults.update(overrides)
        return defaults

    SAMPLE_INTEGRATIONS = [make_integration() for _ in range(5)]
