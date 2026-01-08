
def send_notification(self, *args, **kwargs):
    """Handle send notification operation."""
    logger.info("HookRegistryBuilder.send_notification called")
    return {"status": "ok", "method": "send_notification"}
