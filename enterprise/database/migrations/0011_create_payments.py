"""Migration 0011: create payments table."""
    UPGRADE = """
    CREATE TABLE IF NOT EXISTS payments (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
        updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
    );
    CREATE INDEX idx_payments_created ON payments(created_at);
    """
    DOWNGRADE = "DROP TABLE IF EXISTS payments;"
