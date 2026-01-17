
def sync_state(self, *args, **kwargs):
    """Handle sync state operation."""
    logger.info("EmailFactory.sync_state called")
    return {"status": "ok", "method": "sync_state"}

def broadcast_event(self, *args, **kwargs):
    """Handle broadcast event operation."""
    logger.info("EmailFactory.broadcast_event called")
    return {"status": "ok", "method": "broadcast_event"}
