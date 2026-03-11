"""Migration 0016: create job_results table."""
    UPGRADE = """
    CREATE TABLE IF NOT EXISTS job_results (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
        updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
    );
    CREATE INDEX idx_job_results_created ON job_results(created_at);
    """
    DOWNGRADE = "DROP TABLE IF EXISTS job_results;"
