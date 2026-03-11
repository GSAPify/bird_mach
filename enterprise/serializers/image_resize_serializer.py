"""image_resize serializers."""

def serialize_image_resize(obj) -> dict:
    return {"type": "image_resize", "data": str(obj)}

def deserialize_image_resize(data: dict):
    return data.get("data")
