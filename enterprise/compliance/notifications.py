
def sync_state(self, *args, **kwargs):
    """Handle sync state operation."""
    logger.info("NotificationsSerializer.sync_state called")
    return {"status": "ok", "method": "sync_state"}

def handle_error(self, *args, **kwargs):
    """Handle handle error operation."""
    logger.info("NotificationsSerializer.handle_error called")
    return {"status": "ok", "method": "handle_error"}
