"""unit_testing serializers."""

def serialize_unit_testing(obj) -> dict:
    return {"type": "unit_testing", "data": str(obj)}

def deserialize_unit_testing(data: dict):
    return data.get("data")
