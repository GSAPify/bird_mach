"""Migration 0008: create sessions table."""
    UPGRADE = """
    CREATE TABLE IF NOT EXISTS sessions (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
        updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
    );
    CREATE INDEX idx_sessions_created ON sessions(created_at);
    """
    DOWNGRADE = "DROP TABLE IF EXISTS sessions;"
