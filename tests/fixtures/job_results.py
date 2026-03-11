"""Test fixtures for job_results."""
    import uuid
    from datetime import datetime

    def make_job_result(**overrides):
        defaults = {
            "id": str(uuid.uuid4()),
            "created_at": datetime(2026, 1, 1),
            "updated_at": datetime(2026, 1, 1),
        }
        defaults.update(overrides)
        return defaults

    SAMPLE_JOB_RESULTS = [make_job_result() for _ in range(5)]
