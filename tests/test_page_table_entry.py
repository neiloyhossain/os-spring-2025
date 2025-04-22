import pytest
from models.page_table_entry import PageTableEntry

def test_pte_initialization_defaults():
    """Test PageTableEntry initialization with default values."""
    pte = PageTableEntry(page_number=5)
    assert pte.page_number == 5
    assert pte.frame_number is None
    assert pte.valid_bit is False
    assert pte.reference_bit is False
    assert pte.timestamp == 0
    assert pte.access_count == 0
    assert not pte.is_valid()

def test_pte_initialization_specific():
    """Test PageTableEntry initialization with specific values."""
    pte = PageTableEntry(
        page_number=10,
        frame_number=2,
        valid_bit=True,
        reference_bit=True,
        timestamp=100,
        access_count=3
    )
    assert pte.page_number == 10
    assert pte.frame_number == 2
    assert pte.valid_bit is True
    assert pte.reference_bit is True
    assert pte.timestamp == 100
    assert pte.access_count == 3
    assert pte.is_valid()

def test_pte_update_access():
    """Test updating access information."""
    pte = PageTableEntry(page_number=7)
    pte.update_access(current_time=50)
    assert pte.reference_bit is True
    assert pte.timestamp == 50
    assert pte.access_count == 1
    
    pte.update_access(current_time=75)
    assert pte.reference_bit is True # Should remain true
    assert pte.timestamp == 75 # Should update
    assert pte.access_count == 2 # Should increment

def test_pte_load_in_frame():
    """Test loading a page into a frame."""
    pte = PageTableEntry(page_number=3)
    pte.load_in_frame(frame_number=1, current_time=120)
    
    assert pte.frame_number == 1
    assert pte.valid_bit is True
    assert pte.timestamp == 120
    assert pte.access_count == 1 # Should reset to 1 on load
    assert pte.reference_bit is True
    assert pte.is_valid()

def test_pte_evict():
    """Test evicting a page from a frame."""
    pte = PageTableEntry(
        page_number=9,
        frame_number=4,
        valid_bit=True,
        reference_bit=True,
        timestamp=200,
        access_count=5
    )
    
    freed_frame = pte.evict()
    
    assert freed_frame == 4
    assert pte.frame_number is None
    assert pte.valid_bit is False
    assert pte.reference_bit is False # Should be reset
    assert not pte.is_valid()
    # Timestamp and access_count are typically irrelevant after eviction,
    # but we can check they aren't unintentionally modified.
    assert pte.timestamp == 200 
    assert pte.access_count == 5 