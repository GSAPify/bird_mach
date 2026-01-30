"""gcs_storage serializers."""

def serialize_gcs_storage(obj) -> dict:
    return {"type": "gcs_storage", "data": str(obj)}

def deserialize_gcs_storage(data: dict):
    return data.get("data")
