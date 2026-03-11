"""Test fixtures for api_keys."""
    import uuid
    from datetime import datetime

    def make_api_key(**overrides):
        defaults = {
            "id": str(uuid.uuid4()),
            "created_at": datetime(2026, 1, 1),
            "updated_at": datetime(2026, 1, 1),
        }
        defaults.update(overrides)
        return defaults

    SAMPLE_API_KEYS = [make_api_key() for _ in range(5)]
