"""Migration 0010: create invoices table."""
    UPGRADE = """
    CREATE TABLE IF NOT EXISTS invoices (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
        updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
    );
    CREATE INDEX idx_invoices_created ON invoices(created_at);
    """
    DOWNGRADE = "DROP TABLE IF EXISTS invoices;"
