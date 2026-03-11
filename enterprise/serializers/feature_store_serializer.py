"""feature_store serializers."""

def serialize_feature_store(obj) -> dict:
    return {"type": "feature_store", "data": str(obj)}

def deserialize_feature_store(data: dict):
    return data.get("data")
