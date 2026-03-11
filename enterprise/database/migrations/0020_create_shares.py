"""Migration 0020: create shares table."""
    UPGRADE = """
    CREATE TABLE IF NOT EXISTS shares (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
        updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
    );
    CREATE INDEX idx_shares_created ON shares(created_at);
    """
    DOWNGRADE = "DROP TABLE IF EXISTS shares;"
