"""video_thumb serializers."""

def serialize_video_thumb(obj) -> dict:
    return {"type": "video_thumb", "data": str(obj)}

def deserialize_video_thumb(data: dict):
    return data.get("data")
