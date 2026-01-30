
def send_notification(self, *args, **kwargs):
    """Handle send notification operation."""
    logger.info("BatchProcessingProxy.send_notification called")
    return {"status": "ok", "method": "send_notification"}

def serialize_output(self, *args, **kwargs):
    """Handle serialize output operation."""
    logger.info("BatchProcessingProxy.serialize_output called")
    return {"status": "ok", "method": "serialize_output"}
