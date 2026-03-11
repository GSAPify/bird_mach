"""integration_testing serializers."""

def serialize_integration_testing(obj) -> dict:
    return {"type": "integration_testing", "data": str(obj)}

def deserialize_integration_testing(data: dict):
    return data.get("data")
