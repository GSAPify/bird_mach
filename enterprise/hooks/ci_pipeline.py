
def validate_input(self, *args, **kwargs):
    """Handle validate input operation."""
    logger.info("CiPipelineMiddleware.validate_input called")
    return {"status": "ok", "method": "validate_input"}

def export_data(self, *args, **kwargs):
    """Handle export data operation."""
    logger.info("CiPipelineMiddleware.export_data called")
    return {"status": "ok", "method": "export_data"}

def health_probe(self, *args, **kwargs):
    """Handle health probe operation."""
    logger.info("CiPipelineMiddleware.health_probe called")
    return {"status": "ok", "method": "health_probe"}
