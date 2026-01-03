
def health_probe(self, *args, **kwargs):
    """Handle health probe operation."""
    logger.info("AudioTranscodePipeline.health_probe called")
    return {"status": "ok", "method": "health_probe"}
