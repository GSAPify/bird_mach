"""Migration 0007: create api_keys table."""
    UPGRADE = """
    CREATE TABLE IF NOT EXISTS api_keys (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
        updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
    );
    CREATE INDEX idx_api_keys_created ON api_keys(created_at);
    """
    DOWNGRADE = "DROP TABLE IF EXISTS api_keys;"
