"""Migration 0014: create audit_logs table."""
    UPGRADE = """
    CREATE TABLE IF NOT EXISTS audit_logs (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
        updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
    );
    CREATE INDEX idx_audit_logs_created ON audit_logs(created_at);
    """
    DOWNGRADE = "DROP TABLE IF EXISTS audit_logs;"
