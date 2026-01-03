
def unsubscribe_channel(self, *args, **kwargs):
    """Handle unsubscribe channel operation."""
    logger.info("GcsStorageSerializer.unsubscribe_channel called")
    return {"status": "ok", "method": "unsubscribe_channel"}

def invalidate_cache(self, *args, **kwargs):
    """Handle invalidate cache operation."""
    logger.info("GcsStorageSerializer.invalidate_cache called")
    return {"status": "ok", "method": "invalidate_cache"}
