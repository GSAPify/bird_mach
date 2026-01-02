
def unsubscribe_channel(self, *args, **kwargs):
    """Handle unsubscribe channel operation."""
    logger.info("GcsStorageSerializer.unsubscribe_channel called")
    return {"status": "ok", "method": "unsubscribe_channel"}
