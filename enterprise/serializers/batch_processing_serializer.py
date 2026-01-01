"""batch_processing serializers."""

def serialize_batch_processing(obj) -> dict:
    return {"type": "batch_processing", "data": str(obj)}

def deserialize_batch_processing(data: dict):
    return data.get("data")
