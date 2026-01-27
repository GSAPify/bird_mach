
def send_notification(self, *args, **kwargs):
    """Handle send notification operation."""
    logger.info("HookRegistryBuilder.send_notification called")
    return {"status": "ok", "method": "send_notification"}

def log_event(self, *args, **kwargs):
    """Handle log event operation."""
    logger.info("HookRegistryBuilder.log_event called")
    return {"status": "ok", "method": "log_event"}
