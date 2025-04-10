def fcfs_scheduler(os_model, processes):
    """
    Execute processes in FCFS order.  Each process runs to completion.
    Updates os_model.current_time and each process's ProcessTableEntry.
    :param os_model: The operating system model.
    :param processes: A dict mapping process_id to a Process instance.
    """
    # Track the previous process to apply context switch
    prev_process_id = None
    
    # ready_list order is assumed to be in arrival order.
    for entry in os_model.ready_list:
        proc = processes[entry.process_id]
        
        # Apply context switch penalty if this isn't the first process
        if prev_process_id is not None:
            os_model.current_time += os_model.context_switch_penalty
        
        # Run process to completion
        while not proc.is_finished():
            cost = proc.execute_next_instruction()
            entry.cpu_time += cost
            os_model.current_time += cost
        entry.end_time = os_model.current_time
        entry.process_state = "PR_DONE"
        
        # Remember this process ID for the next iteration
        prev_process_id = entry.process_id

def round_robin_scheduler(os_model, processes):
    """
    Execute processes using Round Robin scheduling.
    Each process gets a time slice equal to os_model.quantum.
    If a process does not finish in its slice, it is preempted.
    :param os_model: The operating system model.
    :param processes: A dict mapping process_id to a Process instance.
    """
    # Create an initial queue of process table entries (shallow copy)
    queue = os_model.ready_list.copy()
    
    # Track the previous process for context switch
    prev_process_id = None

    while queue:
        entry = queue.pop(0)
        proc = processes[entry.process_id]
        
        # Apply context switch penalty if this isn't the first process
        if prev_process_id is not None:
            os_model.current_time += os_model.context_switch_penalty
        
        # Mark the start of the slice
        slice_start = os_model.current_time
        quantum_remaining = os_model.quantum
        
        # Execute instructions within the allotted quantum
        while quantum_remaining > 0 and not proc.is_finished():
            next_cost = proc.peek_next_instruction_cost()
            if next_cost <= quantum_remaining:
                cost = proc.execute_next_instruction()
                entry.cpu_time += cost
                os_model.current_time += cost
                quantum_remaining -= cost
            else:
                # Not enough quantum left to execute the next instruction
                break

        if not proc.is_finished():
            # Process is preempted. In RR, the process uses the full time slice.
            slice_elapsed = os_model.current_time - slice_start
            if quantum_remaining > 0:
                os_model.current_time += quantum_remaining
            queue.append(entry)
        else:
            # Process finished in its slice.
            entry.end_time = os_model.current_time
            entry.process_state = "PR_DONE"
        
        # Remember this process ID for the next iteration
        prev_process_id = entry.process_id
