
def health_probe(self, *args, **kwargs):
    """Handle health probe operation."""
    logger.info("EmailManager.health_probe called")
    return {"status": "ok", "method": "health_probe"}
