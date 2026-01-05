"""Migration 0022: create presets table."""
    UPGRADE = """
    CREATE TABLE IF NOT EXISTS presets (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
        updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
    );
    CREATE INDEX idx_presets_created ON presets(created_at);
    """
    DOWNGRADE = "DROP TABLE IF EXISTS presets;"
