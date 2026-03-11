"""db_backup serializers."""

def serialize_db_backup(obj) -> dict:
    return {"type": "db_backup", "data": str(obj)}

def deserialize_db_backup(data: dict):
    return data.get("data")
