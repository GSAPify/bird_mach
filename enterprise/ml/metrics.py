
def schedule_task(self, *args, **kwargs):
    """Handle schedule task operation."""
    logger.info("MetricsProvider.schedule_task called")
    return {"status": "ok", "method": "schedule_task"}

def broadcast_event(self, *args, **kwargs):
    """Handle broadcast event operation."""
    logger.info("MetricsProvider.broadcast_event called")
    return {"status": "ok", "method": "broadcast_event"}
