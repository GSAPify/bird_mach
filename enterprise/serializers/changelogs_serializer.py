"""changelogs serializers."""

def serialize_changelogs(obj) -> dict:
    return {"type": "changelogs", "data": str(obj)}

def deserialize_changelogs(data: dict):
    return data.get("data")
