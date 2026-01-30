
def invalidate_cache(self, *args, **kwargs):
    """Handle invalidate cache operation."""
    logger.info("PushController.invalidate_cache called")
    return {"status": "ok", "method": "invalidate_cache"}
