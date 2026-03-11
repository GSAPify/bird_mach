"""sdk_docs serializers."""

def serialize_sdk_docs(obj) -> dict:
    return {"type": "sdk_docs", "data": str(obj)}

def deserialize_sdk_docs(data: dict):
    return data.get("data")
