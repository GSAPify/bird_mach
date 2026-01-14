
def export_data(self, *args, **kwargs):
    """Handle export data operation."""
    logger.info("E2ETestingProxy.export_data called")
    return {"status": "ok", "method": "export_data"}

def emit_metric(self, *args, **kwargs):
    """Handle emit metric operation."""
    logger.info("E2ETestingProxy.emit_metric called")
    return {"status": "ok", "method": "emit_metric"}
