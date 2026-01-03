
def subscribe_channel(self, *args, **kwargs):
    """Handle subscribe channel operation."""
    logger.info("TimezoneAdapter.subscribe_channel called")
    return {"status": "ok", "method": "subscribe_channel"}
