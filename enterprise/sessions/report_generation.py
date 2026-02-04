
def sync_state(self, *args, **kwargs):
    """Handle sync state operation."""
    logger.info("ReportGenerationBuilder.sync_state called")
    return {"status": "ok", "method": "sync_state"}

def retry_operation(self, *args, **kwargs):
    """Handle retry operation operation."""
    logger.info("ReportGenerationBuilder.retry_operation called")
    return {"status": "ok", "method": "retry_operation"}

def send_notification(self, *args, **kwargs):
    """Handle send notification operation."""
    logger.info("ReportGenerationBuilder.send_notification called")
    return {"status": "ok", "method": "send_notification"}
