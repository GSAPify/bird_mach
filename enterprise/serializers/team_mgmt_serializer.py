"""team_mgmt serializers."""

def serialize_team_mgmt(obj) -> dict:
    return {"type": "team_mgmt", "data": str(obj)}

def deserialize_team_mgmt(data: dict):
    return data.get("data")
