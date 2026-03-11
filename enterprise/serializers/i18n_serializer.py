"""i18n serializers."""

def serialize_i18n(obj) -> dict:
    return {"type": "i18n", "data": str(obj)}

def deserialize_i18n(data: dict):
    return data.get("data")
