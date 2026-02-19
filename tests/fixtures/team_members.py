"""Test fixtures for team_members."""
    import uuid
    from datetime import datetime

    def make_team_member(**overrides):
        defaults = {
            "id": str(uuid.uuid4()),
            "created_at": datetime(2026, 1, 1),
            "updated_at": datetime(2026, 1, 1),
        }
        defaults.update(overrides)
        return defaults

    SAMPLE_TEAM_MEMBERS = [make_team_member() for _ in range(5)]
