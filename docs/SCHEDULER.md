_These are the oiginal notes from class. Thy may not be reflective of the current implementation. See the [README](../README.md) for the current state of the project._

---
# Modeling and Analysis of OS Scheduling Algorithms

This project implements and analyzes different CPU scheduling algorithms to compare their performance characteristics in various workload scenarios.

## Project Overview

This simulation focuses on analyzing the behavior and performance of different CPU scheduling algorithms by modeling core OS components and running various types of processes. The project aims to provide insights into how different scheduling strategies affect process execution metrics.

## System Components

### Process Model
- Represents a sequence of instructions
- Contains essential state information:
  - Program Counter (PC)
  - Start Time (nanosecond precision using scaled Unix timestamps)

### Instruction Types
- **Memory Operations**
  - Load (100ns)
  - Store (200ns)
- **Arithmetic Operations**
  - Addition (10ns)
  - Subtraction (10ns)
  - Multiplication (20ns)
  - Division (20ns)

### CPU Model
- Maintains current execution state
  - Program Counter (PC)

### Operating System Model
- Data Structures:
  - Process Table - Keeps track of all the processes.
  - Process Table Entry - Keeps track of the process metadata.
    - Process ID
    - Process State - One of PR_CURR, PR_READY.
    - Process Start Time
    - Process End Time
    - CPU Time
  - Readylist - Keeps track of the processes in list.
- Tracks system state:
  - Current Process - The process currently being executed.
  - Current Time - The current time in nanoseconds (maintained by an internal counter).
  - Quatum - The time quantum for scheduling (default: 2ms)
- Implements scheduling algorithms

## Scope Limitations

To maintain focus and simplicity, the following components are not included in the simulation:
- Memory management
- Interrupt handling
- Context switching overhead
- Cache operations

## Experimental Design

### Process Types
The simulation uses four distinct process profiles:
1. **Process A**: Memory-intensive workload
2. **Process B**: CPU-intensive workload
3. **Process C**: Balanced workload (mixed CPU and memory operations)
4. **Process D**: Random instruction mix

### Scheduling Algorithms
Two scheduling approaches are implemented and analyzed:
1. **Sequential Scheduler**: Basic FCFS (First-Come-First-Served) approach
2. **Round Robin**: Time-sliced scheduling with configurable quantum sizes

### Performance Metrics
The following metrics are collected and analyzed:
- **Turnaround Time**: Total time from process creation to completion
- **Waiting Time**: Total time spent waiting in the ready queue

## Analysis Goals

The project aims to:
1. Compare the performance of different scheduling algorithms
2. Analyze how quantum size affects Round Robin scheduling efficiency
3. Identify which scheduling approach works best for different process types
4. Provide insights into scheduling algorithm selection based on workload characteristics

## Getting Started

[Add installation and usage instructions here]

## Contributors

[Add contributor information here]

## License

[Add license information here]



