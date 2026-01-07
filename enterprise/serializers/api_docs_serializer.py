"""api_docs serializers."""

def serialize_api_docs(obj) -> dict:
    return {"type": "api_docs", "data": str(obj)}

def deserialize_api_docs(data: dict):
    return data.get("data")
