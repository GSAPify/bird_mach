"""Migration 0005: create teams table."""
    UPGRADE = """
    CREATE TABLE IF NOT EXISTS teams (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
        updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
    );
    CREATE INDEX idx_teams_created ON teams(created_at);
    """
    DOWNGRADE = "DROP TABLE IF EXISTS teams;"
