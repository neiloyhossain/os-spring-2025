# Project Part 3: Page Table Algorithm Comparison Report

In this third part of the project, you’ll use the OS simulator to compare the performance of different page table replacement algorithms under various memory access patterns.

You’ll run the simulator using the `--part 3 --sweep` flags, which tests FIFO, LRU, and LFU algorithms against random, locality-based, and sequential page reference patterns. **A key part of this assignment is implementing the LRU and LFU algorithms yourself.** You will analyze how the choice of algorithm and the nature of memory access affect performance metrics like hit rate, miss rate, and the total number of page faults.

This is an implementation, experiment, and analysis assignment. You will implement LRU and LFU, generate performance comparison charts using Python, and prepare a brief report explaining the results.

## Prerequisites

*   You have a working Python 3 development environment.
*   You have successfully completed Part 1 and Part 2.
*   You can run `python main.py` successfully.

## Videos

*   Spring 2024 Project Videos *(Link Placeholder)*

## Part 3 Instructions

1.  **Download the Project Part 3 Starter:**
    *   Download `os-2025-spring-project-starter-3.zip` *(Link Placeholder)* from the course materials (e.g., Google Drive, Canvas). This zip file contains the necessary code additions for Part 3, **but the LRU and LFU algorithms are intentionally left incomplete.**

2.  **Update Your Project:**
    *   Unzip the downloaded file.
    *   Carefully copy the contents of the unzipped starter folder into your existing `os-spring-2025` project directory.
    *   **Make sure you replace any existing files** (like `main.py`, `models/operating_system.py`, etc.) with the versions provided in the starter zip to ensure you have the correct Part 3 functionality. Add any new files (like `page_table_sim.py`, `models/page_table.py`, etc.).

3.  **Navigate to Project Directory:** Open your terminal or IDE and navigate to the root directory of your updated `os-spring-2025` project.

4.  **Install Dependencies:** If you haven't already, or if new dependencies were added, ensure you have the necessary Python packages installed. You likely need `matplotlib` and `numpy`. If a `requirements.txt` file exists:
    ```bash
    pip install -r requirements.txt
    ```
    Otherwise, install manually if needed:
    ```bash
    pip install matplotlib numpy
    ```

5.  **Run Tests (Expect Failures):** Before implementing, run the test suite to see the initial state.
    ```bash
    pytest
    ```
    You should see several tests failing with `NotImplementedError` for LRU and LFU. This is expected.

6.  **Implement LRU and LFU:**
    *   Open the file `models/page_table.py`.
    *   Locate the methods `_lru_replace(self)` and `_lfu_replace(self)`.
    *   Implement the logic for the Least Recently Used (LRU) and Least Frequently Used (LFU) page replacement algorithms within these methods. You will need to use the `timestamp` and `access_count` attributes stored in the `PageTableEntry` objects.
    *   Re-run `pytest` periodically to check if your implementations pass the corresponding tests.

7.  **Run the Page Table Comparison Sweep:** Once your LRU and LFU implementations pass the tests, execute the simulation using the `main.py` script with the flags for Part 3 sweep.
    ```bash
    python main.py --part 3 --sweep
    ```
    This command uses the default simulation parameters: 8 frames, 16 pages, and 1000 references per pattern.

8.  **Observe Output:** The simulation will run comparisons for each algorithm (FIFO, LRU, LFU) across each reference pattern (random, locality, sequential). You should see output like:
    ```
    === Running Algorithm Comparison Across Reference Patterns ===
    Settings: 8 frames, 16 pages, 1000 references

    Running comparison for FIFO algorithm...
    Simulating pattern: random
    Generated random sequence of length 1000

    Algorithm: FIFO, Frames: 8, Pattern: Sequence Length 1000
    Page Faults: ...
    Hit Rate: ...%
    Miss Rate: ...%
    ... (similar output for other patterns/algorithms) ...

    Comparison charts saved to output directory.
    ```

9.  **Examine Generated Charts:** Once completed, a set of column charts comparing the algorithms will be saved to your project's `output/` directory:
    *   `hit_rate_comparison.png`: Compares the hit rate of each algorithm for each reference pattern.
    *   `miss_rate_comparison.png`: Compares the miss rate.
    *   `page_faults_comparison.png`: Compares the total number of page faults.

10. **(Optional) Customize Parameters:** You can re-run the sweep with different parameters if desired:
    ```bash
    python main.py --part 3 --sweep --frames 12 --num-pages 32 --sequence-length 5000
    ```

11. **Write Report:** Analyze the key trends observed in the generated charts and write a short report using the template below.

## Report Template (Turn in as report.md or report.pdf)

Your report should be 1-2 pages and include the following 3 sections:

**1. Introduction**
*   What was the goal of this experiment? (i.e., what question were you trying to answer about page replacement algorithms?)
*   What were the key independent variables (things you changed/compared) and dependent variables (metrics you measured)?
*   Briefly describe the reference patterns used (random, locality, sequential).

**2. Key Observations**
*   **Overall Performance:** Based on the charts (hit rate, miss rate, page faults), which algorithm generally performed best? Did the best algorithm change depending on the reference pattern?
*   **Performance per Pattern:**
    *   **Random:** How did FIFO, LRU, and LFU compare on the random reference pattern? Were their performances similar or different?
    *   **Locality:** Which algorithm(s) showed the best performance with the locality pattern? Which performed worst?
    *   **Sequential:** How did the algorithms perform with the sequential access pattern?
*   Summarize the key differences in hit/miss rates and page faults between the algorithms for each pattern type.

**3. Reflection**
*   **Why the Trends?** Explain *why* you think certain algorithms performed better or worse for specific patterns.
    *   Why does LRU typically perform well with locality?
    *   Why might FIFO struggle with certain patterns?
    *   How does LFU's frequency counting affect its performance in these scenarios?
*   **Real-world Implications:** How do these results relate to real-world program behavior and memory access? Which pattern might be most representative of typical applications?
*   **Algorithm Complexity:** Consider the implementation complexity (or overhead) of FIFO, LRU, and LFU. Is the best-performing algorithm always the most practical choice? Discuss the trade-offs.
*   **Non-Linearity:** Were there any significant non-linear differences in performance between the patterns or algorithms? (e.g., did one algorithm perform *much* better/worse on one pattern compared to others?) Why might this occur?

## What to Submit

1.  The three charts generated by the simulator (`hit_rate_comparison.png`, `miss_rate_comparison.png`, `page_faults_comparison.png`).
2.  Your written report (e.g., `report.md`, `report.pdf`).
3.  A screenshot showing the terminal output after running `python main.py --part 3 --sweep`.
4.  Your updated `models/page_table.py` file containing your implemented LRU and LFU algorithms.
5.  (Optional but Recommended) Commit and push your updated code (including tests and the implemented algorithms) and the report materials to your GitHub repository.

## Grading Rubric (Total: 20 points)

*   **5 points – LRU/LFU Implementation:** You successfully implement the `_lru_replace` and `_lfu_replace` methods in `models/page_table.py` such that the corresponding tests pass when running `pytest`.
*   **3 points – Simulation Execution:** You successfully run the page table comparison sweep (`--part 3 --sweep`) after implementing LRU/LFU and generate the required comparison charts.
*   **2 points – Submission:** Charts, report, screenshot, and `page_table.py` file are submitted correctly. (GitHub commit is optional but good practice).
*   **2 points – Report Structure:** Your written report follows the provided template (Introduction, Observations, Reflection).
*   **4 points – Data Analysis:** Your report clearly explains the observed performance trends for each algorithm across the different reference patterns, referencing the generated charts.
*   **4 points – Reflection Quality:** Your reflection thoughtfully discusses the reasons behind the observed trends, considers real-world implications, and addresses algorithm trade-offs.

## Troubleshooting

*   **Failing LRU/LFU Tests?** This is expected initially! You need to implement the `_lru_replace` and `_lfu_replace` methods in `models/page_table.py`. Review the lecture notes and concepts for LRU and LFU page replacement. Use the `pytest` output to debug your implementations.
*   **`main.py` errors?** Ensure you have merged the Part 3 starter code correctly, replacing old files and adding new ones. Check for missing files (`page_table_sim.py`, `models/page_table.py`, etc.).
*   **Import Errors?** Make sure `matplotlib` and `numpy` are installed (`pip install -r requirements.txt` or `pip install matplotlib numpy`). Check your Python environment.
*   **No Charts?** Ensure the simulation completes without errors after implementing LRU/LFU. Check the `output/` directory. Make sure you ran `python main.py --part 3 --sweep`.
*   **Need help?** Ask in class, office hours, or via email.