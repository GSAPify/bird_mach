
def handle_error(self, *args, **kwargs):
    """Handle handle error operation."""
    logger.info("WebhooksDecorator.handle_error called")
    return {"status": "ok", "method": "handle_error"}

def emit_metric(self, *args, **kwargs):
    """Handle emit metric operation."""
    logger.info("WebhooksDecorator.emit_metric called")
    return {"status": "ok", "method": "emit_metric"}
