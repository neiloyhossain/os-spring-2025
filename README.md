# Operating System Simulator

This project simulates and analyzes different aspects of operating system behavior, including CPU scheduling and page table management.

## Features

- **Part 2: CPU Scheduling Simulation**
  - Simulate First-Come-First-Served (FCFS) and Round Robin (RR) scheduling algorithms.
  - Model processes with different instruction mixes (CPU-bound, I/O-bound, balanced).
  - Calculate performance metrics: Turnaround Time, CPU Time, Waiting Time.
  - Perform parameter sweeps to analyze scheduler performance under varying conditions (e.g., quantum values, workload types).
- **Part 3: Page Table Replacement Simulation**
  - Simulate page replacement algorithms: FIFO, LRU, LFU.
  - Configure the number of physical memory frames and virtual pages.
  - Generate different page reference patterns (random, locality, sequential).
  - Compare algorithm performance based on Hit Rate, Miss Rate, and Page Faults.
  - Generate comparison charts visualizing algorithm performance across patterns.

## Project Structure

- **main.py**: Central entry point to run simulations for either Part 2 or Part 3.
- **page_table_sim.py**: Contains logic specific to page table simulations (called by `main.py`).
- **models/**: Core simulation components
  - **operating_system.py**: Main OS model (used by both parts, handles processes, potentially page table).
  - **process.py**: Defines the process model and instruction execution (Part 2).
  - **scheduler.py**: Implements FCFS and RR scheduling algorithms (Part 2).
  - **page_table.py**: Page table implementation with replacement algorithms (Part 3).
  - **page_table_entry.py**: Individual page table entry representation (Part 3).
  - **process_table_entry.py**: Data structure for process metadata (used by both parts).
- **utils/**: Utility modules
  - **parameter_sweep.py**: Implements parameter sweep for scheduler simulations (Part 2).
  - **reference_generator.py**: Generates different types of page reference sequences (Part 3).
  - **process_generator.py**: Generates processes with configurable instruction characteristics (Part 2).
- **data/**: Contains text files with process instructions for Part 2 simulations.
- **output/**: Directory for generated charts and results.

## Usage (via main.py)

The primary way to run simulations is through `main.py`. Use the `--part` argument to select the simulation type.

### Part 2: CPU Scheduling

**1. Run a Single Simulation:**

   - **FCFS (Default):**
     ```bash
     python main.py --part 2
     # or simply:
     python main.py 
     ```
   - **Round Robin:**
     ```bash
     python main.py --part 2 --scheduler rr
     # Specify a different quantum (default: 500 ns)
     python main.py --part 2 --scheduler rr --quantum 300
     ```

**2. Run Scheduler Parameter Sweep:**

   This performs simulations across different workload types and quantum values (for RR), generating analysis charts in `output/`.
   ```bash
   python main.py --part 2 --sweep
   ```

### Part 3: Page Table Replacement

**Run Algorithm Comparison Sweep:**

This compares FIFO, LRU, and LFU algorithms across different reference patterns (random, locality, sequential) and generates charts in `output/`.

   - **Using default parameters (8 frames, 16 pages, 1000 references):**
     ```bash
     python main.py --part 3 --sweep
     ```
   - **Specifying custom parameters:**
     ```bash
     python main.py --part 3 --sweep --frames 12 --num-pages 32 --sequence-length 2000
     ```

## Command Line Options (main.py)

```
usage: main.py [-h] [--part {2,3}] [--sweep] [--scheduler {fcfs,rr}] [--quantum QUANTUM] [--frames FRAMES] [--num-pages NUM_PAGES] [--sequence-length SEQUENCE_LENGTH] [--output-dir OUTPUT_DIR]

OS Simulation Entry Point (Scheduler or Page Table)

options:
  -h, --help            show this help message and exit
  --part {2,3}          Choose the simulation part: '2' for Scheduler (FCFS/RR), '3' for Page Table Comparison. (default: 2)
  --sweep               Run parameter sweep for the selected part. (default: False)
  --output-dir OUTPUT_DIR
                        Directory to save generated charts. (default: output)

Part 2: Scheduler Options:
  --scheduler {fcfs,rr}
                        Choose the scheduler (used only if --part 2 and not --sweep). (default: fcfs)
  --quantum QUANTUM     Time quantum for Round Robin scheduler in ns (used only if --part 2 and scheduler is 'rr'). (default: 500)

Part 3: Page Table Sweep Options (used only if --part 3 and --sweep):
  --frames FRAMES       Number of physical memory frames available. (default: 8)
  --num-pages NUM_PAGES
                        Number of distinct pages in virtual memory. (default: 16)
  --sequence-length SEQUENCE_LENGTH
                        Length of reference sequence for each pattern. (default: 1000)
```

## Output

- **Part 2 (Sweep):** Charts comparing scheduler performance (total time, turnaround, waiting) vs. workload and quantum in the `output/` directory.
- **Part 3 (Sweep):** Column charts comparing page replacement algorithms (hit rate, miss rate, page faults) across reference patterns in the `output/` directory.

