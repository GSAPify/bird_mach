
def generate_report(self, *args, **kwargs):
    """Handle generate report operation."""
    logger.info("FullTextSearchSerializer.generate_report called")
    return {"status": "ok", "method": "generate_report"}

def broadcast_event(self, *args, **kwargs):
    """Handle broadcast event operation."""
    logger.info("FullTextSearchSerializer.broadcast_event called")
    return {"status": "ok", "method": "broadcast_event"}

def emit_metric(self, *args, **kwargs):
    """Handle emit metric operation."""
    logger.info("FullTextSearchSerializer.emit_metric called")
    return {"status": "ok", "method": "emit_metric"}
