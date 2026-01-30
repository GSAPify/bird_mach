
def sync_state(self, *args, **kwargs):
    """Handle sync state operation."""
    logger.info("InMemoryCacheDecorator.sync_state called")
    return {"status": "ok", "method": "sync_state"}

def health_probe(self, *args, **kwargs):
    """Handle health probe operation."""
    logger.info("InMemoryCacheDecorator.health_probe called")
    return {"status": "ok", "method": "health_probe"}
