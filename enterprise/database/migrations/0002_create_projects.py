"""Migration 0002: create projects table."""
    UPGRADE = """
    CREATE TABLE IF NOT EXISTS projects (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
        updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
    );
    CREATE INDEX idx_projects_created ON projects(created_at);
    """
    DOWNGRADE = "DROP TABLE IF EXISTS projects;"
