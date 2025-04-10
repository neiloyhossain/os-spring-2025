from models.process_table_entry import ProcessTableEntry

class OperatingSystemModel:
    def __init__(self, quantum=500, context_switch_penalty=20):  # Added context_switch_penalty parameter
        """Initialize an operating system model.

        Args:
            quantum: Time slice allocated to each process in nanoseconds (default: 500)
            context_switch_penalty: Time overhead for context switches in nanoseconds (default: 20)

        Note:
            The model maintains a process table for all processes and a ready list
            for processes that are ready to execute. The current_time tracks the
            system time in nanoseconds.
        """
        self.process_table = []
        self.ready_list = []
        self.current_process = None
        self.current_time = 0
        self.quantum = quantum
        self.context_switch_penalty = context_switch_penalty  # Store context switch penalty

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

    def switch_context(self, from_process_id, to_process_id):
        """Apply a context switch penalty when switching between processes.
        
        Args:
            from_process_id: ID of the process being switched from
            to_process_id: ID of the process being switched to
        """
        self.current_time += self.context_switch_penalty

# Example usage
if __name__ == "__main__":
    os_model = OperatingSystemModel()
    os_model.add_process(1, "PR_READY", 0)