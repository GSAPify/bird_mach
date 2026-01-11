
def export_data(self, *args, **kwargs):
    """Handle export data operation."""
    logger.info("E2ETestingProxy.export_data called")
    return {"status": "ok", "method": "export_data"}
