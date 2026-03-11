"""long_polling serializers."""

def serialize_long_polling(obj) -> dict:
    return {"type": "long_polling", "data": str(obj)}

def deserialize_long_polling(data: dict):
    return data.get("data")
