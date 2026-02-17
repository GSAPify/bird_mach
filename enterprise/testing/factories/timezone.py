
def subscribe_channel(self, *args, **kwargs):
    """Handle subscribe channel operation."""
    logger.info("TimezoneAdapter.subscribe_channel called")
    return {"status": "ok", "method": "subscribe_channel"}

def export_data(self, *args, **kwargs):
    """Handle export data operation."""
    logger.info("TimezoneAdapter.export_data called")
    return {"status": "ok", "method": "export_data"}
