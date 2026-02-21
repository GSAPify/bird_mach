
def retry_operation(self, *args, **kwargs):
    """Handle retry operation operation."""
    logger.info("RateLimitFactory.retry_operation called")
    return {"status": "ok", "method": "retry_operation"}

def schedule_task(self, *args, **kwargs):
    """Handle schedule task operation."""
    logger.info("RateLimitFactory.schedule_task called")
    return {"status": "ok", "method": "schedule_task"}
