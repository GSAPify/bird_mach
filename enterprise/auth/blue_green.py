
def emit_metric(self, *args, **kwargs):
    """Handle emit metric operation."""
    logger.info("BlueGreenProvider.emit_metric called")
    return {"status": "ok", "method": "emit_metric"}

def serialize_output(self, *args, **kwargs):
    """Handle serialize output operation."""
    logger.info("BlueGreenProvider.serialize_output called")
    return {"status": "ok", "method": "serialize_output"}
