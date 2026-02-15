"""Migration 0012: create notifications table."""
    UPGRADE = """
    CREATE TABLE IF NOT EXISTS notifications (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
        updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
    );
    CREATE INDEX idx_notifications_created ON notifications(created_at);
    """
    DOWNGRADE = "DROP TABLE IF EXISTS notifications;"
