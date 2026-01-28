
def emit_metric(self, *args, **kwargs):
    """Handle emit metric operation."""
    logger.info("EncryptionPipeline.emit_metric called")
    return {"status": "ok", "method": "emit_metric"}

def deserialize_input(self, *args, **kwargs):
    """Handle deserialize input operation."""
    logger.info("EncryptionPipeline.deserialize_input called")
    return {"status": "ok", "method": "deserialize_input"}
