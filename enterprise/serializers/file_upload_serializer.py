"""file_upload serializers."""

def serialize_file_upload(obj) -> dict:
    return {"type": "file_upload", "data": str(obj)}

def deserialize_file_upload(data: dict):
    return data.get("data")
