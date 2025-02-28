import argparse
from models.operating_system import OperatingSystemModel
from models.process_table_entry import ProcessTableEntry
from models.process import Process
from models.scheduler import fcfs_scheduler, round_robin_scheduler

def load_process(file_path, process_id):
    """
    Load the instructions from a process file and create a Process instance.
    """
    with open(file_path, "r") as f:
        lines = f.readlines()
    # Filter out any blank lines
    instructions = [line.strip() for line in lines if line.strip()]
    return Process(process_id, instructions)

def main():
    parser = argparse.ArgumentParser(description="OS Scheduling Simulator")
    parser.add_argument('--scheduler', choices=['fcfs', 'rr'], default='fcfs',
                        help="Choose the scheduler: 'fcfs' for First-Come-First-Served, 'rr' for Round Robin")
    args = parser.parse_args()

    os_model = OperatingSystemModel()  # quantum is 2ms (2,000,000 ns) by default

    # List of process files to load (only 4 processes)
    process_files = [
        "data/process_a.txt",
        "data/process_b.txt",
        "data/process_c.txt",
        "data/process_d.txt"
    ]
    
    processes = {}
    # Create a Process instance for each file and add a ProcessTableEntry to the OS model.
    for i, file_path in enumerate(process_files, start=1):
        proc = load_process(file_path, i)
        processes[i] = proc
        os_model.add_process(i, "PR_READY", os_model.current_time)

    # Run the appropriate scheduler
    if args.scheduler == "fcfs":
        print("Running FCFS scheduler...")
        fcfs_scheduler(os_model, processes)
    else:
        print("Running Round Robin scheduler...")
        round_robin_scheduler(os_model, processes)

    # Display performance metrics for each process
    print("\nProcess Metrics:")
    for entry in os_model.process_table:
        turnaround_time = entry.end_time - entry.start_time if entry.end_time is not None else 0
        waiting_time = turnaround_time - entry.cpu_time
        print(f"Process {entry.process_id}: Turnaround Time = {turnaround_time} ns, "
              f"CPU Time = {entry.cpu_time} ns, Waiting Time = {waiting_time} ns")
    print(f"Total simulation time: {os_model.current_time} ns")

if __name__ == "__main__":
    main()