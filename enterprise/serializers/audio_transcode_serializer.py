"""audio_transcode serializers."""

def serialize_audio_transcode(obj) -> dict:
    return {"type": "audio_transcode", "data": str(obj)}

def deserialize_audio_transcode(data: dict):
    return data.get("data")
