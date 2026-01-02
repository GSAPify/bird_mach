"""db_seeding serializers."""

def serialize_db_seeding(obj) -> dict:
    return {"type": "db_seeding", "data": str(obj)}

def deserialize_db_seeding(data: dict):
    return data.get("data")
