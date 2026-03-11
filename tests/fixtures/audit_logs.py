"""Test fixtures for audit_logs."""
    import uuid
    from datetime import datetime

    def make_audit_log(**overrides):
        defaults = {
            "id": str(uuid.uuid4()),
            "created_at": datetime(2026, 1, 1),
            "updated_at": datetime(2026, 1, 1),
        }
        defaults.update(overrides)
        return defaults

    SAMPLE_AUDIT_LOGS = [make_audit_log() for _ in range(5)]
