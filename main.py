import argparse
from models.operating_system import OperatingSystemModel
# Keep ProcessTableEntry import if needed by OSModel or elsewhere
# from models.process_table_entry import ProcessTableEntry 
from models.process import Process
from models.scheduler import fcfs_scheduler, round_robin_scheduler
from utils.parameter_sweep import perform_parameter_sweep
# Import page table simulation functions
from page_table_sim import compare_reference_patterns, generate_comparison_charts

def load_process(file_path, process_id):
    """
    Load the instructions from a process file and create a Process instance.
    """
    try:
        with open(file_path, "r") as f:
            lines = f.readlines()
        # Filter out any blank lines
        instructions = [line.strip() for line in lines if line.strip()]
        if not instructions:
            print(f"Warning: Process file {file_path} is empty or contains only whitespace.")
            return None
        return Process(process_id, instructions)
    except FileNotFoundError:
        print(f"Error: Process file {file_path} not found.")
        return None
    except Exception as e:
        print(f"Error loading process file {file_path}: {e}")
        return None

def run_scheduler_simulation(args):
    """Runs the FCFS or Round Robin scheduler simulation."""
    # Regular simulation with fixed process files
    os_model = OperatingSystemModel(quantum=args.quantum)

    # List of process files to load (only 4 processes)
    process_files = [
        "data/process_a.txt",
        "data/process_b.txt",
        "data/process_c.txt",
        "data/process_d.txt"
    ]
    
    processes = {}
    # Create a Process instance for each file and add a ProcessTableEntry to the OS model.
    process_count = 0
    for i, file_path in enumerate(process_files, start=1):
        proc = load_process(file_path, i)
        if proc:
            processes[i] = proc
            os_model.add_process(i, "PR_READY", os_model.current_time)
            process_count += 1
        else:
            print(f"Skipping process from file: {file_path}")

    if process_count == 0:
        print("Error: No valid processes loaded. Aborting simulation.")
        return

    # Run the appropriate scheduler
    if args.scheduler == "fcfs":
        print("Running FCFS scheduler...")
        fcfs_scheduler(os_model, processes)
    else:
        print(f"Running Round Robin scheduler with quantum = {args.quantum} ns...")
        round_robin_scheduler(os_model, processes)

    # Display performance metrics for each process
    print("\nProcess Metrics:")
    for entry in os_model.process_table:
        turnaround_time = entry.end_time - entry.start_time if entry.end_time is not None else 0
        waiting_time = turnaround_time - entry.cpu_time
        print(f"Process {entry.process_id}: Turnaround Time = {turnaround_time} ns, "
              f"CPU Time = {entry.cpu_time} ns, Waiting Time = {waiting_time} ns")
    print(f"Total simulation time: {os_model.current_time} ns")

def run_page_table_sweep(args):
    """Runs the page table algorithm comparison sweep."""
    print("\n=== Running Page Table Algorithm Comparison Across Reference Patterns ===")
    print(f"Settings: {args.frames} frames, {args.num_pages} pages, {args.sequence_length} references")
    results = compare_reference_patterns(
        num_frames=args.frames,
        max_page=args.num_pages,
        sequence_length=args.sequence_length
    )
    generate_comparison_charts(results, args.output_dir)

def main():
    parser = argparse.ArgumentParser(
        description="OS Simulation Entry Point (Scheduler or Page Table)",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    # Main simulation type selection
    parser.add_argument('--part', choices=['2', '3'], default='2',
                        help="Choose the simulation part: '2' for Scheduler (FCFS/RR), '3' for Page Table Comparison.")
    parser.add_argument('--sweep', action='store_true',
                        help="Run parameter sweep for the selected part.")

    # Part 2: Scheduler Arguments
    scheduler_group = parser.add_argument_group('Part 2: Scheduler Options')
    scheduler_group.add_argument('--scheduler', choices=['fcfs', 'rr'], default='fcfs',
                                 help="Choose the scheduler (used only if --part 2 and not --sweep).")
    scheduler_group.add_argument('--quantum', type=int, default=500,
                                 help="Time quantum for Round Robin scheduler in ns (used only if --part 2 and scheduler is 'rr').")

    # Part 3: Page Table Sweep Arguments
    page_table_group = parser.add_argument_group('Part 3: Page Table Sweep Options (used only if --part 3 and --sweep)')
    page_table_group.add_argument("--frames", type=int, default=8,
                                  help="Number of physical memory frames available.")
    page_table_group.add_argument("--num-pages", type=int, default=16,
                                  help="Number of distinct pages in virtual memory.")
    page_table_group.add_argument("--sequence-length", type=int, default=1000,
                                  help="Length of reference sequence for each pattern.")
    page_table_group.add_argument("--output-dir", default="output",
                                  help="Directory to save generated charts.")
    
    args = parser.parse_args()
    
    if args.part == '2':
        if args.sweep:
            print("Running Scheduler parameter sweep simulations...")
            perform_parameter_sweep() # Assumes this function handles its own output/charts
        else:
            print("Running single Scheduler simulation...")
            run_scheduler_simulation(args)
    elif args.part == '3':
        if args.sweep:
            run_page_table_sweep(args)
        else:
            print("Error: For --part 3, only the --sweep option is supported to run the page table comparison.")
            parser.print_help()
    else:
        # Should not happen due to choices constraint, but good practice
        print("Error: Invalid part selected.")
        parser.print_help()

if __name__ == "__main__":
    main()