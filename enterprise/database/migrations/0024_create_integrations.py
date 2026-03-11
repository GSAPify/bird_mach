"""Migration 0024: create integrations table."""
    UPGRADE = """
    CREATE TABLE IF NOT EXISTS integrations (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
        updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
    );
    CREATE INDEX idx_integrations_created ON integrations(created_at);
    """
    DOWNGRADE = "DROP TABLE IF EXISTS integrations;"
