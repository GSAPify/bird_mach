"""project_mgmt serializers."""

def serialize_project_mgmt(obj) -> dict:
    return {"type": "project_mgmt", "data": str(obj)}

def deserialize_project_mgmt(data: dict):
    return data.get("data")
