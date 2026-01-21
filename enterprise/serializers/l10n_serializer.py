"""l10n serializers."""

def serialize_l10n(obj) -> dict:
    return {"type": "l10n", "data": str(obj)}

def deserialize_l10n(data: dict):
    return data.get("data")
