"""helm_charts serializers."""

def serialize_helm_charts(obj) -> dict:
    return {"type": "helm_charts", "data": str(obj)}

def deserialize_helm_charts(data: dict):
    return data.get("data")
