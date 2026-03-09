"""Migration 0009: create subscriptions table."""
    UPGRADE = """
    CREATE TABLE IF NOT EXISTS subscriptions (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
        updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
    );
    CREATE INDEX idx_subscriptions_created ON subscriptions(created_at);
    """
    DOWNGRADE = "DROP TABLE IF EXISTS subscriptions;"
