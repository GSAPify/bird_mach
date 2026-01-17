"""ab_testing serializers."""

def serialize_ab_testing(obj) -> dict:
    return {"type": "ab_testing", "data": str(obj)}

def deserialize_ab_testing(data: dict):
    return data.get("data")
