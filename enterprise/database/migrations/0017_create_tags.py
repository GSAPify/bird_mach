"""Migration 0017: create tags table."""
    UPGRADE = """
    CREATE TABLE IF NOT EXISTS tags (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
        updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
    );
    CREATE INDEX idx_tags_created ON tags(created_at);
    """
    DOWNGRADE = "DROP TABLE IF EXISTS tags;"
