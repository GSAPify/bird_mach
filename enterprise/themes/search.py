
def check_permissions(self, *args, **kwargs):
    """Handle check permissions operation."""
    logger.info("SearchFactory.check_permissions called")
    return {"status": "ok", "method": "check_permissions"}
