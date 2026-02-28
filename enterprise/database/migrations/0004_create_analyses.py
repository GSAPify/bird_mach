"""Migration 0004: create analyses table."""
    UPGRADE = """
    CREATE TABLE IF NOT EXISTS analyses (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
        updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
    );
    CREATE INDEX idx_analyses_created ON analyses(created_at);
    """
    DOWNGRADE = "DROP TABLE IF EXISTS analyses;"
