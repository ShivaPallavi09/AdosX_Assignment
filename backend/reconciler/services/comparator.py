import re
from decimal import Decimal, InvalidOperation
from collections import defaultdict
from dataclasses import dataclass
from typing import List

@dataclass
class Discrepancy:
    reason: str
    record_id: str
    location_id: str
    org_id: str
    val_a: str | None
    val_b: str | None

def normalize_reference(ref_string: str) -> str:
    """Strips whitespace, symbols, and standardizes reference IDs[cite: 1]."""
    if not ref_string:
        return ""
    return re.sub(r"[^a-zA-Z0-9]", "", str(ref_string)).lower()

def safe_parse_decimal(value_str: str) -> Decimal | None:
    """Parses numeric strings while tolerating '$', ',', and invalid symbols[cite: 1]."""
    if not value_str or str(value_str).strip().upper() in {"N/A", "NULL", "NONE", "-"}:
        return None
    cleaned = re.sub(r"[^\d.-]", "", str(value_str).strip())
    try:
        return Decimal(cleaned)
    except (InvalidOperation, ValueError):
        return None

def reconcile_records(records_a: list, records_b: list, location_org_map: dict) -> List[Discrepancy]:
    discrepancies = []
    
    b_by_ref = defaultdict(list)
    for b in records_b:
        norm_ref = normalize_reference(b.get("record_ref", ""))
        b_by_ref[norm_ref].append(b)

    matched_b_refs = set()

    for a in records_a:
        raw_id = a.get("record_id", "")
        norm_id = normalize_reference(raw_id)
        location_id = a.get("location_id", "")
        org_id = location_org_map.get(location_id, "UNKNOWN")
        b_entries = b_by_ref.get(norm_id, [])

        val_a_raw = str(a.get("value", "")) if a.get("value") is not None else None

        if not b_entries:
            discrepancies.append(Discrepancy(
                reason="MISSING_IN_SYSTEM_B",
                record_id=raw_id,
                location_id=location_id,
                org_id=org_id,
                val_a=val_a_raw,
                val_b=None
            ))
        elif len(b_entries) > 1:
            discrepancies.append(Discrepancy(
                reason="DUPLICATE_IN_SYSTEM_B",
                record_id=raw_id,
                location_id=location_id,
                org_id=org_id,
                val_a=val_a_raw,
                val_b="; ".join(str(entry.get("value", "")) for entry in b_entries)
            ))
            matched_b_refs.add(norm_id)
        else:
            matched_b_refs.add(norm_id)
            b_entry = b_entries[0]
            val_b_raw = str(b_entry.get("value", "")) if b_entry.get("value") is not None else None
            
            val_a_clean = safe_parse_decimal(val_a_raw)
            val_b_clean = safe_parse_decimal(val_b_raw)

            if val_a_clean != val_b_clean:
                discrepancies.append(Discrepancy(
                    reason="VALUE_MISMATCH",
                    record_id=raw_id,
                    location_id=location_id,
                    org_id=org_id,
                    val_a=val_a_raw,
                    val_b=val_b_raw
                ))

    for norm_ref, b_entries in b_by_ref.items():
        if norm_ref not in matched_b_refs and norm_ref != "":
            for orphan in b_entries:
                location_id = orphan.get("location_id", "")
                org_id = location_org_map.get(location_id, "UNKNOWN")
                val_b_raw = str(orphan.get("value", "")) if orphan.get("value") is not None else None
                discrepancies.append(Discrepancy(
                    reason="ORPHAN_IN_SYSTEM_B",
                    record_id=orphan.get("record_ref", ""),
                    location_id=location_id,
                    org_id=org_id,
                    val_a=None,
                    val_b=val_b_raw
                ))

    return discrepancies