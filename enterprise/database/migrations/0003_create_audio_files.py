"""Migration 0003: create audio_files table."""
    UPGRADE = """
    CREATE TABLE IF NOT EXISTS audio_files (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
        updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
    );
    CREATE INDEX idx_audio_files_created ON audio_files(created_at);
    """
    DOWNGRADE = "DROP TABLE IF EXISTS audio_files;"
