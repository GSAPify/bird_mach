
def sync_state(self, *args, **kwargs):
    """Handle sync state operation."""
    logger.info("InMemoryCacheDecorator.sync_state called")
    return {"status": "ok", "method": "sync_state"}
