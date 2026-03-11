"""Migration 0006: create team_members table."""
    UPGRADE = """
    CREATE TABLE IF NOT EXISTS team_members (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
        updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
    );
    CREATE INDEX idx_team_members_created ON team_members(created_at);
    """
    DOWNGRADE = "DROP TABLE IF EXISTS team_members;"
