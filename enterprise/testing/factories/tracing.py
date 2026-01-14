
def serialize_output(self, *args, **kwargs):
    """Handle serialize output operation."""
    logger.info("TracingWorker.serialize_output called")
    return {"status": "ok", "method": "serialize_output"}

def apply_migration(self, *args, **kwargs):
    """Handle apply migration operation."""
    logger.info("TracingWorker.apply_migration called")
    return {"status": "ok", "method": "apply_migration"}
