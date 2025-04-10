# Modeling and Analysis of OS Scheduling Algorithms

This project simulates and analyzes different CPU scheduling algorithms using a simple operating system model. It demonstrates how various scheduling strategies affect process execution metrics by running simulated processes represented by sequences of instructions.

## Project Overview

The simulation models core OS components and processes to study the impact of scheduling decisions. Two scheduling algorithms are implemented:
- **First-Come-First-Served (FCFS):** Processes run to completion in the order they arrive.
- **Round Robin (RR):** Processes receive fixed time slices (quanta) and may be preempted if they do not finish execution within their allotted time.

## System Components

### Process Model
- Represents a sequence of instructions (e.g., `LOAD`, `ADD`, `STORE`).
- Maintains essential state information including the program counter (PC).

### Instruction Types and Execution Costs
- **Memory Operations**
  - `LOAD`: 10 ns
  - `STORE`: 20 ns
- **Arithmetic Operations**
  - `ADD`: 1 ns
  - `SUB`: 1 ns
  - `MUL`: 5 ns
  - `DIV`: 5 ns

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
  - **Context Switch Penalty:** Default is **20 ns**, representing the overhead of switching between processes.

## Process Profiles

The simulation includes four distinct types of processes:
1. **Process A:** Memory-intensive workload (more `LOAD` and `STORE` operations).
2. **Process B:** CPU-intensive workload (primarily arithmetic operations).
3. **Process C:** Balanced workload (a mix of CPU and memory operations).
4. **Process D:** Random instruction mix providing varied workloads.

Process instruction files are stored in the `data/` directory (e.g., `data/process_a.txt`, `data/process_b.txt`, etc.).

Additionally, the system supports dynamic process generation with configurable workload characteristics:
- A process generator can create processes with a specified number of instructions and CPU vs. memory instruction probability.
- This is particularly useful for the parameter sweep functionality that analyzes scheduling performance across various workload profiles.

## Scheduling Algorithms

- **FCFS Scheduler:** Executes processes in the order they appear in the ready list, running each process to completion. Context switches are applied between processes.
- **Round Robin Scheduler:** Allocates a fixed time slice to each process. If the process cannot complete its next instruction within the remaining quantum, it is preempted and added back to the ready queue. Context switches are applied between time slices.

## Performance Metrics

For each process, the following metrics are captured:
- **Turnaround Time:** Total time from process creation to completion (calculated as `end_time - start_time`).
- **CPU Time:** Total time the process spent executing instructions.
- **Waiting Time:** Time spent waiting in the ready queue (calculated as `turnaround_time - cpu_time`).

The simulation outputs each process's metrics along with the total simulation time.

## Usage

Run the simulation from the command line using:

```
python main.py --scheduler [fcfs | rr]
```

Example:

```
python main.py --scheduler fcfs
```

The `--scheduler` flag lets you choose between the FCFS and Round Robin scheduling approaches.

You can also adjust the Round Robin quantum (default is 500 ns):

```
python main.py --scheduler rr --quantum 300
```

### Parameter Sweep

The project includes a parameter sweep feature that simulates different configurations and generates performance analysis charts:

```
python main.py --sweep
```

This will:
1. Run simulations across a range of CPU vs. memory instruction probabilities (0 to 0.9).
2. For Round Robin, test various quantum values (100 to 900 ns).
3. Generate charts in the `output/` directory showing:
   - Total simulation time vs. CPU probability and quantum
   - Average turnaround time vs. CPU probability and quantum
   - Average waiting time vs. CPU probability and quantum
   - Heatmaps visualizing the relationships between parameters and performance

## Project Structure

- **main.py**: Entry point for the simulation.
- **models/**: Contains the core modules:
  - **process.py**: Defines the process model and instruction execution logic.
  - **operating_system.py**: Implements the OS model that manages the process table, ready list, and context switching.
  - **process_table_entry.py**: Data structure for process metadata.
  - **scheduler.py**: Contains implementations for the FCFS and Round Robin scheduling algorithms.
- **utils/**: Contains utility modules:
  - **process_generator.py**: Generates processes with configurable instruction characteristics.
  - **parameter_sweep.py**: Implements parameter sweep simulations and chart generation.
- **data/**: Contains text files with process instructions.
- **output/**: Directory for generated charts from parameter sweeps.
- **tests/**: Unit tests for all key modules and scheduling functions.
- **.github/workflows/test.yaml**: GitHub Actions configuration for automated testing.

