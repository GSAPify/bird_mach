"""vector_search serializers."""

def serialize_vector_search(obj) -> dict:
    return {"type": "vector_search", "data": str(obj)}

def deserialize_vector_search(data: dict):
    return data.get("data")
