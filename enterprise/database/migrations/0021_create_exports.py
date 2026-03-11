"""Migration 0021: create exports table."""
    UPGRADE = """
    CREATE TABLE IF NOT EXISTS exports (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
        updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
    );
    CREATE INDEX idx_exports_created ON exports(created_at);
    """
    DOWNGRADE = "DROP TABLE IF EXISTS exports;"
