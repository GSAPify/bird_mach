"""fuzzy_match serializers."""

def serialize_fuzzy_match(obj) -> dict:
    return {"type": "fuzzy_match", "data": str(obj)}

def deserialize_fuzzy_match(data: dict):
    return data.get("data")
