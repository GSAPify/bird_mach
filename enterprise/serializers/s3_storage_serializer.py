"""s3_storage serializers."""

def serialize_s3_storage(obj) -> dict:
    return {"type": "s3_storage", "data": str(obj)}

def deserialize_s3_storage(data: dict):
    return data.get("data")
