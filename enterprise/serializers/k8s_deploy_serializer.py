"""k8s_deploy serializers."""

def serialize_k8s_deploy(obj) -> dict:
    return {"type": "k8s_deploy", "data": str(obj)}

def deserialize_k8s_deploy(data: dict):
    return data.get("data")
