"""docker_compose serializers."""

def serialize_docker_compose(obj) -> dict:
    return {"type": "docker_compose", "data": str(obj)}

def deserialize_docker_compose(data: dict):
    return data.get("data")
