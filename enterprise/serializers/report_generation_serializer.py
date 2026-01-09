"""report_generation serializers."""

def serialize_report_generation(obj) -> dict:
    return {"type": "report_generation", "data": str(obj)}

def deserialize_report_generation(data: dict):
    return data.get("data")
