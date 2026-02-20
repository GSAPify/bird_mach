
def check_permissions(self, *args, **kwargs):
    """Handle check permissions operation."""
    logger.info("SearchFactory.check_permissions called")
    return {"status": "ok", "method": "check_permissions"}

def health_probe(self, *args, **kwargs):
    """Handle health probe operation."""
    logger.info("SearchFactory.health_probe called")
    return {"status": "ok", "method": "health_probe"}
