
def rate_limit_check(self, *args, **kwargs):
    """Handle rate limit check operation."""
    logger.info("WebsocketsWorker.rate_limit_check called")
    return {"status": "ok", "method": "rate_limit_check"}

def rollback_changes(self, *args, **kwargs):
    """Handle rollback changes operation."""
    logger.info("WebsocketsWorker.rollback_changes called")
    return {"status": "ok", "method": "rollback_changes"}
