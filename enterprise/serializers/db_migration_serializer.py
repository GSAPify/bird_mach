"""db_migration serializers."""

def serialize_db_migration(obj) -> dict:
    return {"type": "db_migration", "data": str(obj)}

def deserialize_db_migration(data: dict):
    return data.get("data")
