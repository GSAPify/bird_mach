"""event_bus serializers."""

def serialize_event_bus(obj) -> dict:
    return {"type": "event_bus", "data": str(obj)}

def deserialize_event_bus(data: dict):
    return data.get("data")
