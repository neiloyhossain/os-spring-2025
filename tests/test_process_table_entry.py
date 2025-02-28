import pytest
from models.process_table_entry import ProcessTableEntry

def test_process_table_entry_initialization():
    # Test basic initialization
    process = ProcessTableEntry(
        process_id=1,
        process_state="PR_READY",
        start_time=100
    )
    
    assert process.process_id == 1
    assert process.process_state == "PR_READY"
    assert process.start_time == 100
    assert process.end_time is None
    assert process.cpu_time == 0

def test_process_table_entry_with_all_parameters():
    # Test initialization with all optional parameters
    process = ProcessTableEntry(
        process_id=2,
        process_state="PR_CURR",
        start_time=200,
        end_time=300,
        cpu_time=50
    )
    
    assert process.process_id == 2
    assert process.process_state == "PR_CURR"
    assert process.start_time == 200
    assert process.end_time == 300
    assert process.cpu_time == 50

def test_process_table_entry_turnaround_time():
    # Test calculation of turnaround time (end_time - start_time)
    process = ProcessTableEntry(
        process_id=3,
        process_state="PR_CURR",
        start_time=100,
        end_time=200,
        cpu_time=60
    )
    
    turnaround_time = process.end_time - process.start_time
    assert turnaround_time == 100

def test_process_table_entry_waiting_time():
    # Test calculation of waiting time (turnaround_time - cpu_time)
    process = ProcessTableEntry(
        process_id=4,
        process_state="PR_CURR",
        start_time=100,
        end_time=300,
        cpu_time=50
    )
    
    turnaround_time = process.end_time - process.start_time
    waiting_time = turnaround_time - process.cpu_time
    assert waiting_time == 150 