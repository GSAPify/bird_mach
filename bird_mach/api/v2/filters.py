"""Query filter parsing and application for API v2."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass
class Filter:
    field: str
    operator: str
    value: str | float | int

VALID_OPERATORS = {"eq", "ne", "gt", "gte", "lt", "lte", "contains", "in"}


def _as_float(value) -> float | None:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None

def parse_filters(query_params: dict[str, str]) -> list[Filter]:
    filters = []
    for key, value in query_params.items():
        if "__" in key:
            field, op = key.rsplit("__", 1)
            if op in VALID_OPERATORS:
                filters.append(Filter(field=field, operator=op, value=value))
        else:
            filters.append(Filter(field=key, operator="eq", value=value))
    return filters

def apply_filters(items: list[dict], filters: list[Filter]) -> list[dict]:
    result = items
    for f in filters:
        if f.operator == "eq":
            result = [i for i in result if str(i.get(f.field)) == str(f.value)]
        elif f.operator == "ne":
            result = [i for i in result if str(i.get(f.field)) != str(f.value)]
        elif f.operator == "gt":
            result = [
                i for i in result
                if (lhs := _as_float(i.get(f.field))) is not None
                and (rhs := _as_float(f.value)) is not None
                and lhs > rhs
            ]
        elif f.operator == "gte":
            result = [
                i for i in result
                if (lhs := _as_float(i.get(f.field))) is not None
                and (rhs := _as_float(f.value)) is not None
                and lhs >= rhs
            ]
        elif f.operator == "lt":
            result = [
                i for i in result
                if (lhs := _as_float(i.get(f.field))) is not None
                and (rhs := _as_float(f.value)) is not None
                and lhs < rhs
            ]
        elif f.operator == "lte":
            result = [
                i for i in result
                if (lhs := _as_float(i.get(f.field))) is not None
                and (rhs := _as_float(f.value)) is not None
                and lhs <= rhs
            ]
        elif f.operator == "contains":
            result = [i for i in result if str(f.value).lower() in str(i.get(f.field, "")).lower()]
        elif f.operator == "in":
            wanted = {v.strip() for v in str(f.value).split(",") if v.strip()}
            result = [i for i in result if str(i.get(f.field)) in wanted]
    return result
