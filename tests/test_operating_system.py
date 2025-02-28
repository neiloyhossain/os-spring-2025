import pytest
from models.operating_system import OperatingSystemModel

def test_operating_system_initial_state():
    os_model = OperatingSystemModel()
    assert os_model.current_time == 0
    # Default quantum is 500 (ns) as defined in the __init__
    assert os_model.quantum == 500
    assert os_model.process_table == []
    assert os_model.ready_list == []

def test_add_process_ready():
    os_model = OperatingSystemModel()
    os_model.add_process(1, "PR_READY", 100)
    # ProcessTableEntry should be added to both process_table and ready_list.
    assert len(os_model.process_table) == 1
    assert len(os_model.ready_list) == 1
    entry = os_model.process_table[0]
    assert entry.process_id == 1
    assert entry.process_state == "PR_READY"
    assert entry.start_time == 100
    # For a ready process, end_time should be None and cpu_time 0
    assert entry.end_time is None
    assert entry.cpu_time == 0

def test_add_process_non_ready():
    os_model = OperatingSystemModel()
    os_model.add_process(2, "PR_CURR", 200)
    # Only processes in state "PR_READY" are added to ready_list.
    assert len(os_model.process_table) == 1
    assert len(os_model.ready_list) == 0
    entry = os_model.process_table[0]
    assert entry.process_state == "PR_CURR"
    assert entry.start_time == 200 