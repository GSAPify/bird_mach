"""Migration 0025: create plugins table."""
    UPGRADE = """
    CREATE TABLE IF NOT EXISTS plugins (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
        updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
    );
    CREATE INDEX idx_plugins_created ON plugins(created_at);
    """
    DOWNGRADE = "DROP TABLE IF EXISTS plugins;"
