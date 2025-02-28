# Modeling and Analysis of OS Scheduling Algorithms

This project simulates and analyzes different CPU scheduling algorithms using a simple operating system model. It demonstrates how various scheduling strategies affect process execution metrics by running simulated processes represented by sequences of instructions.

## Project Overview

The simulation models core OS components and processes to study the impact of scheduling decisions. Two scheduling algorithms are implemented:
- **First-Come-First-Served (FCFS):** Processes run to completion in the order they arrive.
- **Round Robin (RR):** Processes receive fixed time slices (quanta) and may be preempted if they do not finish execution within their allotted time.

## System Components

### Process Model
- Represents a sequence of instructions (e.g., `LOAD`, `ADD`, `STORE`).
- Maintains essential state information including the program counter (PC) and a start time (with nanosecond precision).

### Instruction Types and Execution Costs
- **Memory Operations**
  - `LOAD`: 100 ns
  - `STORE`: 200 ns
- **Arithmetic Operations**
  - `ADD`: 10 ns
  - `SUB`: 10 ns
  - `MUL`: 20 ns
  - `DIV`: 20 ns

### CPU Model
- Keeps track of the current execution state via the program counter.

### Operating System Model
- Maintains a **Process Table** for all processes and a **Ready List** for those that are ready to run.
- Each process is recorded using a **Process Table Entry** which includes:
  - **Process ID**
  - **Process State**
    - `PR_READY`: The process is ready to be scheduled.
    - `PR_CURR`: The process is currently running.
    - `PR_DONE`: The process has finished execution.
  - **Start Time:** When the process is created.
  - **End Time:** When the process completes.
  - **CPU Time:** The total time the process spent executing instructions.
- Tracks overall system state:
  - **Current Process:** The process currently being executed.
  - **Current Time:** The system time in nanoseconds.
  - **Time Quantum:** For Round Robin scheduling, the default quantum is set to **500 ns** (this can be adjusted during OS model initialization).

## Process Profiles

The simulation includes four distinct types of processes:
1. **Process A:** Memory-intensive workload (more `LOAD` and `STORE` operations).
2. **Process B:** CPU-intensive workload (primarily arithmetic operations).
3. **Process C:** Balanced workload (a mix of CPU and memory operations).
4. **Process D:** Random instruction mix providing varied workloads.

Process instruction files are stored in the `data/` directory (e.g., `data/process_a.txt`, `data/process_b.txt`, etc.).

## Scheduling Algorithms

- **FCFS Scheduler:** Executes processes in the order they appear in the ready list, running each process to completion.
- **Round Robin Scheduler:** Allocates a fixed time slice to each process. If the process cannot complete its next instruction within the remaining quantum, it is preempted and added back to the ready queue. Any unused quantum is simulated as idle time.

## Performance Metrics

For each process, the following metrics are captured:
- **Turnaround Time:** Total time from process creation to completion (calculated as `end_time - start_time`).
- **CPU Time:** Total time the process spent executing instructions.
- **Waiting Time:** Time spent waiting in the ready queue (calculated as `turnaround_time - cpu_time`).

The simulation outputs each process's metrics along with the total simulation time.

## Usage

Run the simulation from the command line using:

  python main.py --scheduler [fcfs | rr]

Example:

  python main.py --scheduler fcfs

The `--scheduler` flag lets you choose between the FCFS and Round Robin scheduling approaches.

## Running Tests

This project uses pytest for unit testing. To run all tests, install pytest (if necessary) and execute:

  pytest tests/

## Project Structure

- **main.py**: Entry point for the simulation.
- **models/**: Contains the core modules:
  - **process.py**: Defines the process model and instruction execution logic.
  - **operating_system.py**: Implements the OS model that manages the process table and ready list.
  - **process_table_entry.py**: Data structure for process metadata.
  - **scheduler.py**: Contains implementations for the FCFS and Round Robin scheduling algorithms.
- **data/**: Contains text files with process instructions.
- **tests/**: Unit tests for all key modules and scheduling functions.
- **.github/workflows/test.yaml**: GitHub Actions configuration for automated testing.

## Contributors

[Add contributor information here]

## License

[Add license information here]



