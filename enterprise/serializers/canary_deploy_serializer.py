"""canary_deploy serializers."""

def serialize_canary_deploy(obj) -> dict:
    return {"type": "canary_deploy", "data": str(obj)}

def deserialize_canary_deploy(data: dict):
    return data.get("data")
