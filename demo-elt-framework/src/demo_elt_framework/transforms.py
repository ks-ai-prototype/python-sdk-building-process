from __future__ import annotations

import re
from datetime import datetime
from typing import Any, Callable, Iterable, Optional


_NON_ALNUM = re.compile(r"[^a-z0-9_]+")
_MULTI_UNDERSCORE = re.compile(r"_+")


def clean_columns(columns: Iterable[str]) -> list[str]:
    """Normalize column names (strip, lowercase, spaces->underscore, remove specials)."""
    out: list[str] = []
    for c in columns:
        c = str(c).strip().lower()
        c = c.replace(" ", "_")
        c = _NON_ALNUM.sub("_", c)
        c = _MULTI_UNDERSCORE.sub("_", c).strip("_")
        out.append(c)
    return out


def safe_cast(value: Any, caster: Callable[[Any], Any], default: Any = None) -> Any:
    """Cast value using `caster`; return `default` if it fails."""
    try:
        return caster(value)
    except Exception:
        return default


def trim_strings(records: list[dict[str, Any]], fields: Optional[Iterable[str]] = None) -> list[dict[str, Any]]:
    """Trim whitespace for string fields in a list of dict records."""
    fields_set = set(fields) if fields is not None else None
    out: list[dict[str, Any]] = []
    for r in records:
        nr = dict(r)
        for k, v in r.items():
            if fields_set is not None and k not in fields_set:
                continue
            if isinstance(v, str):
                nr[k] = v.strip()
        out.append(nr)
    return out


def drop_nulls(records: list[dict[str, Any]], fields: Optional[Iterable[str]] = None) -> list[dict[str, Any]]:
    """Drop records where any selected field is None/''."""
    fields_list = list(fields) if fields is not None else None
    out: list[dict[str, Any]] = []
    for r in records:
        keys = fields_list if fields_list is not None else list(r.keys())
        if any(r.get(k) is None or r.get(k) == "" for k in keys):
            continue
        out.append(r)
    return out


def dedupe(records: list[dict[str, Any]], key_fields: Iterable[str]) -> list[dict[str, Any]]:
    """Deduplicate records by key_fields, keeping first occurrence."""
    keys = list(key_fields)
    seen: set[tuple[Any, ...]] = set()
    out: list[dict[str, Any]] = []
    for r in records:
        sig = tuple(r.get(k) for k in keys)
        if sig in seen:
            continue
        seen.add(sig)
        out.append(r)
    return out


def rename_keys(record: dict[str, Any], mapping: dict[str, str]) -> dict[str, Any]:
    """Rename keys in a dict using mapping {old: new}."""
    out: dict[str, Any] = {}
    for k, v in record.items():
        out[mapping.get(k, k)] = v
    return out


def parse_date(value: Any, formats: Optional[list[str]] = None, *, default: Any = None) -> Any:
    """Parse a date from a string using common formats."""
    if value is None:
        return default
    if isinstance(value, datetime):
        return value
    s = str(value).strip()
    fmts = formats or ["%Y-%m-%d", "%d-%m-%Y", "%d/%m/%Y", "%Y/%m/%d", "%Y-%m-%d %H:%M:%S"]
    for f in fmts:
        try:
            return datetime.strptime(s, f)
        except ValueError:
            pass
    return default
