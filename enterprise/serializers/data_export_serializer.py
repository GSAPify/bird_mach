"""data_export serializers."""

def serialize_data_export(obj) -> dict:
    return {"type": "data_export", "data": str(obj)}

def deserialize_data_export(data: dict):
    return data.get("data")
