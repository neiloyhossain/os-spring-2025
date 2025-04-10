from models.scheduler import fcfs_scheduler, round_robin_scheduler
from models.operating_system import OperatingSystemModel
from models.process import Process

def test_fcfs_scheduler():
    # Create an OS model and two dummy processes:
    # Process 1: instructions cost = 10 (LOAD) + 1 (ADD) + 20 (STORE) = 31 ns
    # Process 2: instructions cost = 10 (LOAD) + 5 (MUL) + 5 (DIV) = 20 ns
    # Set context_switch_penalty to 0 to match the original test expectations
    os_model = OperatingSystemModel(context_switch_penalty=0)
    instructions1 = ["LOAD", "ADD", "STORE"]
    instructions2 = ["LOAD", "MUL", "DIV"]
    proc1 = Process(1, instructions1)
    proc2 = Process(2, instructions2)
    processes = {1: proc1, 2: proc2}

    # Add processes to the OS model.
    os_model.add_process(1, "PR_READY", os_model.current_time)
    os_model.add_process(2, "PR_READY", os_model.current_time)

    fcfs_scheduler(os_model, processes)

    # The current_time should be the sum of the two process costs: 31 + 20 = 51
    assert os_model.current_time == 51

    # Check that cpu_time and state have been updated.
    for entry in os_model.process_table:
        if entry.process_id == 1:
            assert entry.cpu_time == 31
            assert entry.end_time is not None
            assert entry.process_state == "PR_DONE"
        elif entry.process_id == 2:
            assert entry.cpu_time == 20
            assert entry.end_time is not None
            assert entry.process_state == "PR_DONE"

def test_round_robin_scheduler_single_process():
    # Test Round Robin with one process that fits in one time slice.
    quantum = 200  # Set a small quantum.
    # No context switch needed for a single process
    os_model = OperatingSystemModel(quantum=quantum, context_switch_penalty=0)
    # Process instructions: "LOAD"(10), "ADD"(1), "STORE"(20) total = 31 ns.
    instructions = ["LOAD", "ADD", "STORE"]
    proc = Process(1, instructions)
    processes = {1: proc}
    os_model.add_process(1, "PR_READY", os_model.current_time)

    round_robin_scheduler(os_model, processes)

    entry = os_model.process_table[0]
    # Since the process finishes within one slice, no idle time is added.
    assert entry.cpu_time == 31
    assert entry.end_time == 31
    assert entry.process_state == "PR_DONE"
    assert os_model.current_time == 31

def test_round_robin_scheduler_multiple_processes():
    # Test Round Robin scheduling with two processes.
    quantum = 200
    # Set context_switch_penalty to 0 to match the original test expectations
    os_model = OperatingSystemModel(quantum=quantum, context_switch_penalty=0)
    # Process 1: ["LOAD", "ADD", "STORE"] => 10 + 1 + 20 = 31 ns
    # Process 2: ["ADD", "SUB", "ADD", "STORE"] => 1 + 1 + 1 + 20 = 23 ns
    instructions1 = ["LOAD", "ADD", "STORE"]
    instructions2 = ["ADD", "SUB", "ADD", "STORE"]
    proc1 = Process(1, instructions1)
    proc2 = Process(2, instructions2)
    processes = {1: proc1, 2: proc2}

    os_model.add_process(1, "PR_READY", os_model.current_time)
    os_model.add_process(2, "PR_READY", os_model.current_time)

    round_robin_scheduler(os_model, processes)

    # Process 1 should complete in its round with cost 31.
    # Process 2 should complete in its round with cost 23.
    # Round 1: Process 1 finishes at time 31.
    # Round 2: Process 2 starts at time 31 and finishes at time 31 + 23 = 54.
    for entry in os_model.process_table:
        if entry.process_id == 1:
            assert entry.cpu_time == 31
            assert entry.end_time == 31
            assert entry.process_state == "PR_DONE"
        elif entry.process_id == 2:
            assert entry.cpu_time == 23
            assert entry.end_time == 54
            assert entry.process_state == "PR_DONE"

    assert os_model.current_time == 54 