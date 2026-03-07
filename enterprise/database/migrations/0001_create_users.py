"""Migration 0001: create users table."""
    UPGRADE = """
    CREATE TABLE IF NOT EXISTS users (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
        updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
    );
    CREATE INDEX idx_users_created ON users(created_at);
    """
    DOWNGRADE = "DROP TABLE IF EXISTS users;"
