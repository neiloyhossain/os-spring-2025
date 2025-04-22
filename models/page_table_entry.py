class PageTableEntry:
    def __init__(self, page_number, frame_number=None, valid_bit=False, reference_bit=False, timestamp=0, access_count=0):
        """Initialize a page table entry.

        Args:
            page_number: Unique identifier for the page
            frame_number: Physical memory frame number where page is loaded (default: None)
            valid_bit: Indicates if the page is currently in memory (default: False)
            reference_bit: Used for tracking page access (default: False)
            timestamp: Time of last access for LRU algorithm (default: 0)
            access_count: Number of accesses for LFU algorithm (default: 0)

        Note:
            The valid_bit indicates whether the page is currently loaded in physical memory.
            The reference_bit, timestamp, and access_count are used by different
            page replacement algorithms.
        """
        self.page_number = page_number
        self.frame_number = frame_number
        self.valid_bit = valid_bit
        self.reference_bit = reference_bit
        self.timestamp = timestamp
        self.access_count = access_count

    def is_valid(self):
        """Check if the page is currently in memory.

        Returns:
            True if the page is in memory, False otherwise.
        """
        return self.valid_bit

    def update_access(self, current_time):
        """Update access information when page is referenced.

        Args:
            current_time: Current system time for timestamp update
        """
        self.reference_bit = True
        self.timestamp = current_time
        self.access_count += 1

    def load_in_frame(self, frame_number, current_time):
        """Load the page into a physical memory frame.

        Args:
            frame_number: Physical memory frame to load the page into
            current_time: Current system time for timestamp update
        """
        self.frame_number = frame_number
        self.valid_bit = True
        self.timestamp = current_time
        self.access_count = 1
        self.reference_bit = True

    def evict(self):
        """Remove the page from memory.

        Returns:
            The frame number that was freed.
        """
        frame = self.frame_number
        self.frame_number = None
        self.valid_bit = False
        self.reference_bit = False
        return frame