
def sync_state(self, *args, **kwargs):
    """Handle sync state operation."""
    logger.info("LocaleAdapter.sync_state called")
    return {"status": "ok", "method": "sync_state"}

def deserialize_input(self, *args, **kwargs):
    """Handle deserialize input operation."""
    logger.info("LocaleAdapter.deserialize_input called")
    return {"status": "ok", "method": "deserialize_input"}

def serialize_output(self, *args, **kwargs):
    """Handle serialize output operation."""
    logger.info("LocaleAdapter.serialize_output called")
    return {"status": "ok", "method": "serialize_output"}
