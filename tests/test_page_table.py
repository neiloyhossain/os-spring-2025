import pytest
from models.page_table import PageTable

# Test sequence from PART3.md for LRU with 4 frames
LRU_EXAMPLE_SEQUENCE = [1, 3, 0, 3, 5, 6, 3, 0, 1, 4, 3, 0, 6]
LRU_EXAMPLE_FRAMES = 4
LRU_EXPECTED_FAULTS = 8

def test_page_table_initialization():
    """Test PageTable initialization."""
    pt = PageTable(num_frames=10, algorithm="LRU")
    assert pt.num_frames == 10
    assert pt.algorithm == "LRU"
    assert len(pt.available_frames) == 10
    assert pt.available_frames == list(range(10))
    assert pt.page_entries == {}
    assert pt.allocated_frames == {}
    assert pt.page_hits == 0
    assert pt.page_faults == 0
    assert pt.total_references == 0
    assert pt.frame_queue == []

def test_page_table_access_hit():
    """Test page access resulting in a hit."""
    pt = PageTable(num_frames=2, algorithm="FIFO")
    # Load page 1 into frame 0
    is_fault_1, frame_1 = pt.access_page(page_number=1, current_time=10)
    assert is_fault_1 is True
    assert frame_1 == 0
    assert pt.page_faults == 1
    assert pt.page_hits == 0
    assert pt.total_references == 1
    assert pt.page_entries[1].access_count == 1
    assert pt.page_entries[1].timestamp == 10

    # Access page 1 again (hit)
    is_fault_2, frame_2 = pt.access_page(page_number=1, current_time=20)
    assert is_fault_2 is False
    assert frame_2 == 0
    assert pt.page_faults == 1 # No change
    assert pt.page_hits == 1
    assert pt.total_references == 2
    assert pt.page_entries[1].access_count == 2 # Incremented
    assert pt.page_entries[1].timestamp == 20 # Updated

def test_page_table_access_miss_available_frame():
    """Test page access resulting in a miss with available frames."""
    pt = PageTable(num_frames=2, algorithm="FIFO")
    # Load page 1 into frame 0
    pt.access_page(page_number=1, current_time=10)
    assert pt.available_frames == [1]
    assert pt.allocated_frames == {0: 1}
    assert pt.frame_queue == [0]

    # Access page 2 (miss, load into frame 1)
    is_fault, frame = pt.access_page(page_number=2, current_time=20)
    assert is_fault is True
    assert frame == 1
    assert pt.page_faults == 2
    assert pt.page_hits == 0
    assert pt.total_references == 2
    assert pt.available_frames == [] # No more available
    assert pt.allocated_frames == {0: 1, 1: 2}
    assert pt.frame_queue == [0, 1]
    assert pt.page_entries[2].access_count == 1
    assert pt.page_entries[2].timestamp == 20

def test_page_table_fifo_replacement():
    """Test page replacement using FIFO algorithm."""
    pt = PageTable(num_frames=2, algorithm="FIFO")
    pt.access_page(page_number=1, current_time=10) # Load 1 -> F0, Q=[0]
    pt.access_page(page_number=2, current_time=20) # Load 2 -> F1, Q=[0, 1]
    assert pt.allocated_frames == {0: 1, 1: 2}

    # Access page 3 (miss, replace page 1 in F0)
    is_fault, frame = pt.access_page(page_number=3, current_time=30)
    assert is_fault is True
    assert frame == 0 # Frame 0 was freed by FIFO
    assert pt.page_faults == 3
    assert pt.available_frames == []
    assert pt.allocated_frames == {0: 3, 1: 2} # Page 3 loaded into F0
    assert pt.frame_queue == [1, 0] # F0 removed, F0 added to end
    assert pt.page_entries[1].is_valid() is False # Page 1 evicted
    assert pt.page_entries[3].is_valid() is True
    assert pt.page_entries[3].frame_number == 0

def test_page_table_lru_replacement():
    """Test page replacement using LRU algorithm."""
    pt = PageTable(num_frames=2, algorithm="LRU")
    pt.access_page(page_number=1, current_time=10) # Load 1 -> F0, T1=10
    pt.access_page(page_number=2, current_time=20) # Load 2 -> F1, T2=20
    pt.access_page(page_number=1, current_time=30) # Hit 1 -> T1=30
    assert pt.allocated_frames == {0: 1, 1: 2}
    assert pt.page_entries[1].timestamp == 30
    assert pt.page_entries[2].timestamp == 20

    # Access page 3 (miss, replace page 2 in F1, as it has older timestamp 20)
    is_fault, frame = pt.access_page(page_number=3, current_time=40)
    assert is_fault is True
    assert frame == 1 # Frame 1 freed by LRU (page 2)
    assert pt.page_faults == 3
    assert pt.available_frames == []
    assert pt.allocated_frames == {0: 1, 1: 3} # Page 3 loaded into F1
    assert pt.page_entries[2].is_valid() is False # Page 2 evicted
    assert pt.page_entries[3].is_valid() is True
    assert pt.page_entries[3].frame_number == 1
    assert pt.page_entries[3].timestamp == 40

def test_page_table_lfu_replacement():
    """Test page replacement using LFU algorithm."""
    pt = PageTable(num_frames=2, algorithm="LFU")
    pt.access_page(page_number=1, current_time=10) # Load 1 -> F0, C1=1
    pt.access_page(page_number=2, current_time=20) # Load 2 -> F1, C2=1
    pt.access_page(page_number=1, current_time=30) # Hit 1 -> C1=2
    pt.access_page(page_number=1, current_time=35) # Hit 1 -> C1=3
    pt.access_page(page_number=2, current_time=40) # Hit 2 -> C2=2
    assert pt.allocated_frames == {0: 1, 1: 2}
    assert pt.page_entries[1].access_count == 3
    assert pt.page_entries[2].access_count == 2

    # Access page 3 (miss, replace page 2 in F1, as it has lower count 2)
    is_fault, frame = pt.access_page(page_number=3, current_time=50)
    assert is_fault is True
    assert frame == 1 # Frame 1 freed by LFU (page 2)
    assert pt.page_faults == 3
    assert pt.available_frames == []
    assert pt.allocated_frames == {0: 1, 1: 3} # Page 3 loaded into F1
    assert pt.page_entries[2].is_valid() is False # Page 2 evicted
    assert pt.page_entries[3].is_valid() is True
    assert pt.page_entries[3].frame_number == 1
    assert pt.page_entries[3].access_count == 1 # Reset to 1 on load

def test_page_table_metrics():
    """Test calculation of performance metrics."""
    pt = PageTable(num_frames=2, algorithm="LRU")
    assert pt.get_hit_rate() == 0.0
    assert pt.get_miss_rate() == 0.0
    assert pt.get_memory_utilization() == 0.0
    
    pt.access_page(1, 10) # Miss
    pt.access_page(2, 20) # Miss
    pt.access_page(1, 30) # Hit
    pt.access_page(3, 40) # Miss (replace 2)
    
    assert pt.total_references == 4
    assert pt.page_hits == 1
    assert pt.page_faults == 3
    assert pt.get_hit_rate() == pytest.approx(25.0)  # 1/4
    assert pt.get_miss_rate() == pytest.approx(75.0)  # 3/4
    assert pt.get_memory_utilization() == pytest.approx(100.0) # 2/2 frames used
    
    metrics = pt.get_metrics()
    assert metrics["total_references"] == 4
    assert metrics["page_hits"] == 1
    assert metrics["page_faults"] == 3
    assert metrics["hit_rate"] == pytest.approx(25.0)
    assert metrics["miss_rate"] == pytest.approx(75.0)
    assert metrics["memory_utilization"] == pytest.approx(100.0)