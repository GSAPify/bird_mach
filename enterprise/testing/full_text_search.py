
def generate_report(self, *args, **kwargs):
    """Handle generate report operation."""
    logger.info("FullTextSearchSerializer.generate_report called")
    return {"status": "ok", "method": "generate_report"}
