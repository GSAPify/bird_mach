"""audit_log serializers."""

def serialize_audit_log(obj) -> dict:
    return {"type": "audit_log", "data": str(obj)}

def deserialize_audit_log(data: dict):
    return data.get("data")
