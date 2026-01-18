
def check_permissions(self, *args, **kwargs):
    """Handle check permissions operation."""
    logger.info("TeamMgmtWorker.check_permissions called")
    return {"status": "ok", "method": "check_permissions"}

def cache_result(self, *args, **kwargs):
    """Handle cache result operation."""
    logger.info("TeamMgmtWorker.cache_result called")
    return {"status": "ok", "method": "cache_result"}
