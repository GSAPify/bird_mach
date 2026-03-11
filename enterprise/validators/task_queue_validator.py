"""task_queue validators."""

def validate_task_queue(data: dict) -> list[str]:
    errors = []
    if not data:
        errors.append("task_queue data is required")
    return errors
