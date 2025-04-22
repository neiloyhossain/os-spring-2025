from models.process_table_entry import ProcessTableEntry
from models.page_table import PageTable

class OperatingSystemModel:
    def __init__(self, quantum=500, context_switch_penalty=20, num_frames=4, page_replacement_algorithm="FIFO", page_fault_penalty=100):
        """Initialize an operating system model.

        Args:
            quantum: Time slice allocated to each process in nanoseconds (default: 500)
            context_switch_penalty: Time overhead for context switches in nanoseconds (default: 20)
            num_frames: Number of physical memory frames available (default: 4)
            page_replacement_algorithm: Algorithm for page replacement (default: FIFO)
            page_fault_penalty: Time overhead for handling page faults in nanoseconds (default: 100)

        Note:
            The model maintains a process table for all processes and a ready list
            for processes that are ready to execute. The current_time tracks the
            system time in nanoseconds. The page table manages memory allocation
            and page replacement.
        """
        self.process_table = []
        self.ready_list = []
        self.page_table = PageTable(num_frames, page_replacement_algorithm)
        self.current_process = None
        self.current_time = 0
        self.quantum = quantum
        self.context_switch_penalty = context_switch_penalty
        self.page_fault_penalty = page_fault_penalty

    def add_process(self, process_id, process_state, start_time):
        """Add a new process to the operating system.

        Args:
            process_id: Unique identifier for the process
            process_state: Initial state of the process (e.g., PR_READY)
            start_time: Time when process is created
        """
        entry = ProcessTableEntry(process_id, process_state, start_time)
        self.process_table.append(entry)
        if process_state == "PR_READY":
            self.ready_list.append(entry)

    def access_memory(self, page_number):
        """Access a memory page and handle page faults.
        
        Args:
            page_number: The page number to access
            
        Returns:
            Tuple of (access_time, frame_number)
        """
        access_time = 0
        is_page_fault, frame_number = self.page_table.access_page(page_number, self.current_time)
        
        # If page fault occurred, add penalty
        if is_page_fault:
            access_time += self.page_fault_penalty
            self.current_time += self.page_fault_penalty
        
        return access_time, frame_number

    def read_memory(self, page_number):
        """Read from a memory page.
        
        Args:
            page_number: The page number to read from
            
        Returns:
            Tuple of (access_time, frame_number)
        """
        return self.access_memory(page_number)

    def write_memory(self, page_number):
        """Write to a memory page.
        
        Args:
            page_number: The page number to write to
            
        Returns:
            Tuple of (access_time, frame_number)
        """
        return self.access_memory(page_number)

    def handle_page_fault(self, page_number):
        """Handle a page fault by loading the page into memory.
        
        Args:
            page_number: The page number that caused the fault
            
        Returns:
            Frame number where the page was loaded
        """
        _, frame_number = self.page_table.access_page(page_number, self.current_time)
        self.current_time += self.page_fault_penalty
        return frame_number

    def get_memory_metrics(self):
        """Get memory performance metrics.
        
        Returns:
            Dictionary of performance metrics
        """
        return self.page_table.get_metrics()

    def switch_context(self, from_process_id, to_process_id):
        """Apply a context switch penalty when switching between processes.
        
        Args:
            from_process_id: ID of the process being switched from
            to_process_id: ID of the process being switched to
        """
        self.current_time += self.context_switch_penalty

    def simulate_page_reference_sequence(self, sequence, algorithm=None):
        """Simulate a sequence of page references with a specific algorithm.
        
        Args:
            sequence: List of page numbers to access
            algorithm: Page replacement algorithm to use (overwrites current if provided)
            
        Returns:
            Dictionary of performance metrics after simulation
        """
        if algorithm:
            old_algorithm = self.page_table.algorithm
            self.page_table = PageTable(self.page_table.num_frames, algorithm)
        
        for page_number in sequence:
            self.access_memory(page_number)
            self.current_time += 1  # Increment time for each access
        
        return self.get_memory_metrics()

# Example usage
if __name__ == "__main__":
    os_model = OperatingSystemModel(num_frames=4, page_replacement_algorithm="LRU")
    os_model.add_process(1, "PR_READY", 0)
    
    # Example page reference sequence from PART3.md
    sequence = [1, 3, 0, 3, 5, 6, 3, 0, 1, 4, 3, 0, 6]
    metrics = os_model.simulate_page_reference_sequence(sequence)
    
    print(f"Page Faults: {metrics['page_faults']}")
    print(f"Hit Rate: {metrics['hit_rate']:.2f}%")
    print(f"Miss Rate: {metrics['miss_rate']:.2f}%")