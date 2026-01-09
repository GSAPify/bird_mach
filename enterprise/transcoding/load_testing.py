
def rollback_changes(self, *args, **kwargs):
    """Handle rollback changes operation."""
    logger.info("LoadTestingBuilder.rollback_changes called")
    return {"status": "ok", "method": "rollback_changes"}
