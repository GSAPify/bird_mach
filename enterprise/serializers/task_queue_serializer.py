"""task_queue serializers."""

def serialize_task_queue(obj) -> dict:
    return {"type": "task_queue", "data": str(obj)}

def deserialize_task_queue(data: dict):
    return data.get("data")
