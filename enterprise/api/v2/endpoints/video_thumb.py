
def schedule_task(self, *args, **kwargs):
    """Handle schedule task operation."""
    logger.info("VideoThumbClient.schedule_task called")
    return {"status": "ok", "method": "schedule_task"}
