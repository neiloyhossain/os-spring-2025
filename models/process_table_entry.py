class ProcessTableEntry:
    def __init__(self, process_id, process_state, start_time, end_time=None, cpu_time=0):
        """Initialize a process table entry.

        Args:
            process_id: Unique identifier for the process
            process_state: Current state of the process (PR_CURR, PR_READY)
            start_time: Time when process was created
            end_time: Time when process completed (default: None)
            cpu_time: Total CPU time used by process (default: 0)

        Note:
            The turnaround time can be calculated as (end_time - start_time).
            The waiting time can be calculated as (turnaround time - cpu_time).
        """
        self.process_id = process_id
        self.process_state = process_state
        self.start_time = start_time
        self.end_time = end_time
        self.cpu_time = cpu_time