from models.page_table_entry import PageTableEntry


class PageTable:
    def __init__(self, num_frames=4, algorithm="FIFO"):
        """Initialize a page table.

        Args:
            num_frames: Number of physical memory frames available (default: 4)
            algorithm: Page replacement algorithm to use (FIFO, LRU, LFU) (default: FIFO)

        Note:
            The page table maintains a mapping of pages to frames and handles page
            replacement according to the specified algorithm.
        """
        self.page_entries = {}  # Map of page_number to PageTableEntry
        self.num_frames = num_frames
        self.algorithm = algorithm.upper()
        self.available_frames = list(range(num_frames))  # List of free frame numbers
        self.allocated_frames = {}  # Map of frame_number to page_number

        # Performance metrics
        self.page_hits = 0
        self.page_faults = 0
        self.total_references = 0

        # For FIFO algorithm
        self.frame_queue = []  # Queue of frame numbers in order of allocation

    def access_page(self, page_number, current_time):
        """Access a page and handle page faults if necessary.

        Args:
            page_number: The page number to access
            current_time: Current system time

        Returns:
            Tuple of (is_page_fault, frame_number)
        """
        self.total_references += 1

        # Check if page exists in the page table
        if page_number not in self.page_entries:
            self.page_entries[page_number] = PageTableEntry(page_number)

        entry = self.page_entries[page_number]

        # Check if page is already in memory
        if entry.is_valid():
            self.page_hits += 1
            entry.update_access(current_time)
            return False, entry.frame_number

        # Page fault - page is not in memory
        self.page_faults += 1

        # Check if there are available frames
        if self.available_frames:
            frame_number = self.available_frames.pop(0)
        else:
            # Need to evict a page using the selected algorithm
            frame_number = self._replace_page(current_time)

        # Load the page into the frame
        entry.load_in_frame(frame_number, current_time)
        self.allocated_frames[frame_number] = page_number

        # For FIFO algorithm
        if self.algorithm == "FIFO":
            self.frame_queue.append(frame_number)

        return True, frame_number

    def _replace_page(self, current_time):
        """Replace a page according to the selected algorithm.

        Args:
            current_time: Current system time

        Returns:
            Frame number that was freed
        """
        if self.algorithm == "FIFO":
            return self._fifo_replace()
        elif self.algorithm == "LRU":
            return self._lru_replace()
        elif self.algorithm == "LFU":
            return self._lfu_replace()
        else:
            # Default to FIFO
            return self._fifo_replace()

    def _fifo_replace(self):
        """Implement FIFO page replacement.

        Returns:
            Frame number that was freed
        """
        frame_to_evict = self.frame_queue.pop(0)
        page_to_evict = self.allocated_frames[frame_to_evict]

        # Evict the page
        entry = self.page_entries[page_to_evict]
        entry.evict()

        # Remove from allocated frames
        del self.allocated_frames[frame_to_evict]

        return frame_to_evict

    def _lru_replace(self):
        """Implement LRU page replacement.
        Returns:
            Frame number that was freed
        """
    # Find the frame with the oldest last-access time
        oldest_time = float("inf")
        victim_frame = None

        for frame_number, page_number in self.allocated_frames.items():
            entry = self.page_entries[page_number]
            if entry.timestamp < oldest_time:
                oldest_time = entry.timestamp
                victim_frame = frame_number

        # Evict the page
        page_to_evict = self.allocated_frames[victim_frame]
        self.page_entries[page_to_evict].evict()
        del self.allocated_frames[victim_frame]
        return victim_frame

    def _lfu_replace(self):
        """Implement LFU page replacement.

        Returns:
            Frame number that was freed
        """

    # Find the frame with the least frequently accessed page
        lowest_count = float("inf")
        oldest_time = float("inf")
        victim_frame = None

        for frame_number, page_number in self.allocated_frames.items():
            entry = self.page_entries[page_number]
            if (entry.access_count < lowest_count) or (
                entry.access_count == lowest_count and entry.timestamp < oldest_time
            ):
                lowest_count = entry.access_count
                oldest_time = entry.timestamp
                victim_frame = frame_number
    # Evict the page
        page_to_evict = self.allocated_frames[victim_frame]
        self.page_entries[page_to_evict].evict()
        del self.allocated_frames[victim_frame]
        return victim_frame

    def get_hit_rate(self):
        """Calculate the page hit rate.

        Returns:
            Hit rate as a percentage
        """
        if self.total_references == 0:
            return 0.0
        return (self.page_hits / self.total_references) * 100.0

    def get_miss_rate(self):
        """Calculate the page miss rate.

        Returns:
            Miss rate as a percentage
        """
        if self.total_references == 0:
            return 0.0
        return (self.page_faults / self.total_references) * 100.0

    def get_memory_utilization(self):
        """Calculate the memory utilization.

        Returns:
            Memory utilization as a percentage
        """
        if self.num_frames == 0:
            return 0.0
        return (len(self.allocated_frames) / self.num_frames) * 100.0

    def get_metrics(self):
        """Get all performance metrics.

        Returns:
            Dictionary of performance metrics
        """
        return {
            "hit_rate": self.get_hit_rate(),
            "miss_rate": self.get_miss_rate(),
            "page_faults": self.page_faults,
            "page_hits": self.page_hits,
            "total_references": self.total_references,
            "memory_utilization": self.get_memory_utilization(),
        }
