"""Migration 0023: create user_presets table."""
    UPGRADE = """
    CREATE TABLE IF NOT EXISTS user_presets (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
        updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
    );
    CREATE INDEX idx_user_presets_created ON user_presets(created_at);
    """
    DOWNGRADE = "DROP TABLE IF EXISTS user_presets;"
