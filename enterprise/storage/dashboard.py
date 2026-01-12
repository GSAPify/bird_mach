
def schedule_task(self, *args, **kwargs):
    """Handle schedule task operation."""
    logger.info("DashboardClient.schedule_task called")
    return {"status": "ok", "method": "schedule_task"}

def cleanup_resources(self, *args, **kwargs):
    """Handle cleanup resources operation."""
    logger.info("DashboardClient.cleanup_resources called")
    return {"status": "ok", "method": "cleanup_resources"}
