"""azure_blob serializers."""

def serialize_azure_blob(obj) -> dict:
    return {"type": "azure_blob", "data": str(obj)}

def deserialize_azure_blob(data: dict):
    return data.get("data")
