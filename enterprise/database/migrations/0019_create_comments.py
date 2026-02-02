"""Migration 0019: create comments table."""
    UPGRADE = """
    CREATE TABLE IF NOT EXISTS comments (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
        updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
    );
    CREATE INDEX idx_comments_created ON comments(created_at);
    """
    DOWNGRADE = "DROP TABLE IF EXISTS comments;"
