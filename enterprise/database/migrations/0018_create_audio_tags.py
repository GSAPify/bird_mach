"""Migration 0018: create audio_tags table."""
    UPGRADE = """
    CREATE TABLE IF NOT EXISTS audio_tags (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
        updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
    );
    CREATE INDEX idx_audio_tags_created ON audio_tags(created_at);
    """
    DOWNGRADE = "DROP TABLE IF EXISTS audio_tags;"
