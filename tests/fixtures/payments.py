"""Test fixtures for payments."""
    import uuid
    from datetime import datetime

    def make_payment(**overrides):
        defaults = {
            "id": str(uuid.uuid4()),
            "created_at": datetime(2026, 1, 1),
            "updated_at": datetime(2026, 1, 1),
        }
        defaults.update(overrides)
        return defaults

    SAMPLE_PAYMENTS = [make_payment() for _ in range(5)]
