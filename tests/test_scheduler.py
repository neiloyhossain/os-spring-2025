from models.scheduler import fcfs_scheduler, round_robin_scheduler
from models.operating_system import OperatingSystemModel
from models.process import Process

def test_fcfs_scheduler():
    # Create an OS model and two dummy processes:
    # Process 1: instructions cost = 100 (LOAD) + 10 (ADD) + 200 (STORE) = 310
    # Process 2: instructions cost = 100 (LOAD) + 20 (MUL) + 20 (DIV) = 140
    os_model = OperatingSystemModel()
    instructions1 = ["LOAD", "ADD", "STORE"]
    instructions2 = ["LOAD", "MUL", "DIV"]
    proc1 = Process(1, instructions1)
    proc2 = Process(2, instructions2)
    processes = {1: proc1, 2: proc2}

    # Add processes to the OS model.
    os_model.add_process(1, "PR_READY", os_model.current_time)
    os_model.add_process(2, "PR_READY", os_model.current_time)

    fcfs_scheduler(os_model, processes)

    # The current_time should be the sum of the two process costs.
    # 310 + 140 = 450
    assert os_model.current_time == 450

    # Check that cpu_time and state have been updated.
    for entry in os_model.process_table:
        if entry.process_id == 1:
            assert entry.cpu_time == 310
            assert entry.end_time is not None
            assert entry.process_state == "PR_DONE"
        elif entry.process_id == 2:
            assert entry.cpu_time == 140
            assert entry.end_time is not None
            assert entry.process_state == "PR_DONE"

def test_round_robin_scheduler_single_process():
    # Test Round Robin with one process that requires preemption (multiple rounds).
    quantum = 200  # Set a small quantum to force preemption.
    os_model = OperatingSystemModel(quantum=quantum)
    # Process instructions: "LOAD"(100), "ADD"(10), "STORE"(200)
    # Expected behavior:
    #   Round 1: "LOAD" (100) then "ADD" (10) execute => 110 used, leaving quantum_remaining = 90.
    #            Since "STORE" (200) cannot execute, the remaining 90 ns are added as idle time.
    #            End of round 1: current_time becomes 200 (0 + 110 + 90) and process is requeued.
    #   Round 2: Process executes "STORE" (200) exactly; current_time becomes 400.
    # Thus, total CPU time = 310 and process finishes with end_time = 400.
    instructions = ["LOAD", "ADD", "STORE"]
    proc = Process(1, instructions)
    processes = {1: proc}
    os_model.add_process(1, "PR_READY", os_model.current_time)

    round_robin_scheduler(os_model, processes)

    entry = os_model.process_table[0]
    assert entry.cpu_time == 310
    assert entry.end_time == 400
    assert entry.process_state == "PR_DONE"
    assert os_model.current_time == 400

def test_round_robin_scheduler_multiple_processes():
    # Test Round Robin scheduling with two processes.
    quantum = 200
    os_model = OperatingSystemModel(quantum=quantum)
    # Process 1: ["LOAD", "ADD", "STORE"] => 100 + 10 + 200 = 310
    # Process 2: ["ADD", "SUB", "ADD", "STORE"] => 10 + 10 + 10 + 200 = 230
    instructions1 = ["LOAD", "ADD", "STORE"]
    instructions2 = ["ADD", "SUB", "ADD", "STORE"]
    proc1 = Process(1, instructions1)
    proc2 = Process(2, instructions2)
    processes = {1: proc1, 2: proc2}

    os_model.add_process(1, "PR_READY", os_model.current_time)
    os_model.add_process(2, "PR_READY", os_model.current_time)

    round_robin_scheduler(os_model, processes)

    # Expected simulation (step-by-step):
    # Round 1 (Process 1):
    #   Executes "LOAD"(100) and "ADD"(10) = 110 executed, idle time = 90 ns → current_time becomes 200.
    # Round 2 (Process 2):
    #   Executes "ADD"(10), "SUB"(10), "ADD"(10) = 30 executed, idle time = 170 ns → current_time becomes 400.
    # Round 3 (Process 1):
    #   Executes "STORE"(200) exactly → current_time becomes 600, process1 finishes.
    # Round 4 (Process 2):
    #   Executes "STORE"(200) exactly → current_time becomes 800, process2 finishes.
    for entry in os_model.process_table:
        if entry.process_id == 1:
            assert entry.cpu_time == 310
            assert entry.end_time == 600
            assert entry.process_state == "PR_DONE"
        elif entry.process_id == 2:
            assert entry.cpu_time == 230
            assert entry.end_time == 800
            assert entry.process_state == "PR_DONE"

    assert os_model.current_time == 800 