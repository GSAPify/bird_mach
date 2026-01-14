
def health_probe(self, *args, **kwargs):
    """Handle health probe operation."""
    logger.info("EmailManager.health_probe called")
    return {"status": "ok", "method": "health_probe"}

def send_notification(self, *args, **kwargs):
    """Handle send notification operation."""
    logger.info("EmailManager.send_notification called")
    return {"status": "ok", "method": "send_notification"}
