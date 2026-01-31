"""Test fixtures for jobs."""
    import uuid
    from datetime import datetime

    def make_job(**overrides):
        defaults = {
            "id": str(uuid.uuid4()),
            "created_at": datetime(2026, 1, 1),
            "updated_at": datetime(2026, 1, 1),
        }
        defaults.update(overrides)
        return defaults

    SAMPLE_JOBS = [make_job() for _ in range(5)]
