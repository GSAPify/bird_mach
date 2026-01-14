
def schedule_task(self, *args, **kwargs):
    """Handle schedule task operation."""
    logger.info("VideoThumbClient.schedule_task called")
    return {"status": "ok", "method": "schedule_task"}

def cache_result(self, *args, **kwargs):
    """Handle cache result operation."""
    logger.info("VideoThumbClient.cache_result called")
    return {"status": "ok", "method": "cache_result"}
