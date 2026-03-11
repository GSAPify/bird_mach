"""Migration 0015: create jobs table."""
    UPGRADE = """
    CREATE TABLE IF NOT EXISTS jobs (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
        updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
    );
    CREATE INDEX idx_jobs_created ON jobs(created_at);
    """
    DOWNGRADE = "DROP TABLE IF EXISTS jobs;"
