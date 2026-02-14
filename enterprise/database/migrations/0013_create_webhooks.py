"""Migration 0013: create webhooks table."""
    UPGRADE = """
    CREATE TABLE IF NOT EXISTS webhooks (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
        updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
    );
    CREATE INDEX idx_webhooks_created ON webhooks(created_at);
    """
    DOWNGRADE = "DROP TABLE IF EXISTS webhooks;"
