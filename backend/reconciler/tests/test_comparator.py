import pytest
from reconciler.services.comparator import reconcile_records

def test_detects_record_missing_in_system_b():
    records_a = [{"record_id": "REC-01", "value": 100, "location_id": "LOC-1"}]
    records_b = []
    location_map = {"LOC-1": "ORG-1"}

    results = reconcile_records(records_a, records_b, location_map)
    assert len(results) == 1
    assert results[0].reason == "MISSING_IN_SYSTEM_B"
    assert results[0].record_id == "REC-01"
    assert results[0].org_id == "ORG-1"

def test_detects_orphan_record_in_system_b():
    records_a = []
    records_b = [{"record_ref": "REC-999", "value": 250, "location_id": "LOC-1"}]
    location_map = {"LOC-1": "ORG-1"}

    results = reconcile_records(records_a, records_b, location_map)
    assert len(results) == 1
    assert results[0].reason == "ORPHAN_IN_SYSTEM_B"
    assert results[0].record_id == "REC-999"
    assert results[0].org_id == "ORG-1"

def test_detects_duplicate_entries_in_system_b():
    records_a = [{"record_id": "REC-01", "value": 100, "location_id": "LOC-1"}]
    records_b = [
        {"record_ref": "REC-01", "value": 100, "location_id": "LOC-1"},
        {"record_ref": " rec-01 ", "value": 100, "location_id": "LOC-1"}
    ]
    location_map = {"LOC-1": "ORG-1"}

    results = reconcile_records(records_a, records_b, location_map)
    assert len(results) == 1
    assert results[0].reason == "DUPLICATE_IN_SYSTEM_B"

def test_detects_value_mismatch_with_dirty_data():
    records_a = [{"record_id": "REC-01", "value": "$100.00", "location_id": "LOC-1"}]
    records_b = [{"record_ref": "REC-01", "value": " 120.00 ", "location_id": "LOC-1"}]
    location_map = {"LOC-1": "ORG-1"}

    results = reconcile_records(records_a, records_b, location_map)
    assert len(results) == 1
    assert results[0].reason == "VALUE_MISMATCH"
    assert results[0].val_a == "$100.00"
    assert results[0].val_b == " 120.00 "

def test_ignores_matching_records():
    records_a = [{"record_id": "REC-01", "value": "100.50", "location_id": "LOC-1"}]
    records_b = [{"record_ref": "rec01", "value": "$100.50", "location_id": "LOC-1"}]
    location_map = {"LOC-1": "ORG-1"}

    results = reconcile_records(records_a, records_b, location_map)
    assert len(results) == 0

def test_tenant_boundary_isolation_mapping():
    records_a = [{"record_id": "REC-01", "value": 100, "location_id": "LOC-2"}]
    records_b = []
    location_map = {"LOC-1": "ORG-1", "LOC-2": "ORG-2"}

    results = reconcile_records(records_a, records_b, location_map)
    assert len(results) == 1
    assert results[0].org_id == "ORG-2"