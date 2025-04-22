import pytest
from models.operating_system import OperatingSystemModel
from models.page_table import PageTable # Import for mocking if needed

def test_operating_system_initial_state():
    os_model = OperatingSystemModel()
    assert os_model.current_time == 0
    # Default quantum is 500 (ns) as defined in the __init__
    assert os_model.quantum == 500
    assert os_model.context_switch_penalty == 20 # Default
    assert os_model.page_fault_penalty == 100 # Default
    assert os_model.process_table == []
    assert os_model.ready_list == []
    assert isinstance(os_model.page_table, PageTable)
    assert os_model.page_table.num_frames == 4 # Default
    assert os_model.page_table.algorithm == "FIFO" # Default

def test_operating_system_initialization_custom():
    """Test OS initialization with custom parameters."""
    os_model = OperatingSystemModel(
        quantum=300,
        context_switch_penalty=30,
        num_frames=8,
        page_replacement_algorithm="LRU",
        page_fault_penalty=150
    )
    assert os_model.quantum == 300
    assert os_model.context_switch_penalty == 30
    assert os_model.page_fault_penalty == 150
    assert os_model.page_table.num_frames == 8
    assert os_model.page_table.algorithm == "LRU"

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

def test_switch_context():
    os_model = OperatingSystemModel(context_switch_penalty=25)
    os_model.add_process(1, "PR_CURR", 0) # Assume P1 was running
    os_model.add_process(2, "PR_READY", 0)
    initial_time = os_model.current_time
    os_model.switch_context(from_process_id=1, to_process_id=2)
    assert os_model.current_time == initial_time + 25

def test_access_memory_hit():
    """Test memory access resulting in a page hit."""
    os_model = OperatingSystemModel(num_frames=2, page_fault_penalty=150)
    # Pre-load page 5 into frame 0
    os_model.page_table.access_page(5, current_time=0) 
    initial_time = os_model.current_time # Time might increase due to fault penalty above
    initial_hits = os_model.page_table.page_hits
    
    access_time, frame_num = os_model.access_memory(page_number=5)
    
    assert access_time == 0 # No penalty for a hit
    assert frame_num == 0 # Should be the frame where page 5 is
    assert os_model.current_time == initial_time # System time should not advance on hit
    assert os_model.page_table.page_hits == initial_hits + 1

def test_access_memory_miss():
    """Test memory access resulting in a page fault."""
    os_model = OperatingSystemModel(num_frames=1, page_fault_penalty=150)
    initial_time = os_model.current_time
    initial_faults = os_model.page_table.page_faults
    
    # Access page 7 (miss)
    access_time, frame_num = os_model.access_memory(page_number=7)
    
    assert access_time == 150 # Penalty applied
    assert frame_num == 0 # Should be loaded into the only frame
    assert os_model.current_time == initial_time + 150 # System time advances
    assert os_model.page_table.page_faults == initial_faults + 1
    assert os_model.page_table.page_entries[7].is_valid() is True

def test_read_write_memory():
    """Test read and write memory calls - they should behave like access_memory."""
    os_model = OperatingSystemModel(num_frames=1, page_fault_penalty=120)
    
    # Test read (miss)
    read_time, read_frame = os_model.read_memory(page_number=10)
    assert read_time == 120
    assert read_frame == 0
    time_after_read = os_model.current_time
    assert time_after_read == 120
    
    # Test write (hit)
    write_time, write_frame = os_model.write_memory(page_number=10)
    assert write_time == 0
    assert write_frame == 0
    # Time shouldn't advance further on hit
    assert os_model.current_time == time_after_read 

def test_handle_page_fault():
    """Test the handle_page_fault method (redundant with access_memory miss test but good practice)."""
    os_model = OperatingSystemModel(num_frames=1, page_fault_penalty=111)
    initial_time = os_model.current_time
    initial_faults = os_model.page_table.page_faults
    
    frame_num = os_model.handle_page_fault(page_number=8)
    
    assert frame_num == 0
    assert os_model.current_time == initial_time + 111 # System time advances
    assert os_model.page_table.page_faults == initial_faults + 1
    assert os_model.page_table.page_entries[8].is_valid() is True

def test_get_memory_metrics():
    """Test retrieving memory metrics from the OS model."""
    os_model = OperatingSystemModel(num_frames=2)
    os_model.access_memory(1) # Miss
    os_model.access_memory(2) # Miss
    os_model.access_memory(1) # Hit
    
    metrics = os_model.get_memory_metrics()
    assert metrics["total_references"] == 3
    assert metrics["page_hits"] == 1
    assert metrics["page_faults"] == 2
    assert metrics["hit_rate"] == pytest.approx((1/3) * 100.0)
    assert metrics["miss_rate"] == pytest.approx((2/3) * 100.0)
    assert metrics["memory_utilization"] == pytest.approx(100.0)

def test_simulate_page_reference_sequence():
    """Test simulating a full sequence through the OS model."""
    os_model = OperatingSystemModel(num_frames=4, page_replacement_algorithm="LRU")
    sequence = [1, 3, 0, 3, 5, 6, 3, 0, 1, 4, 3, 0, 6] # Example from PART3.md
    expected_faults = 8
    expected_hits = len(sequence) - expected_faults
    
    metrics = os_model.simulate_page_reference_sequence(sequence)
    
    assert metrics["page_faults"] == expected_faults
    assert metrics["page_hits"] == expected_hits
    assert metrics["total_references"] == len(sequence)
    assert metrics["miss_rate"] == pytest.approx((expected_faults / len(sequence)) * 100.0)
    assert metrics["hit_rate"] == pytest.approx((expected_hits / len(sequence)) * 100.0)
    # Check if time advanced correctly (1 per access + fault penalties)
    # Expected time = base accesses + fault penalties
    # Base accesses = len(sequence) * 1
    # Fault penalties = expected_faults * page_fault_penalty (default 100)
    expected_time = len(sequence) * 1 + expected_faults * 100
    assert os_model.current_time == expected_time 