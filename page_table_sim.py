#!/usr/bin/env python3
"""
Page Table Replacement Algorithm Simulations

This script simulates different page replacement algorithms (FIFO, LRU, LFU)
and compares their performance metrics across different reference patterns.
"""

import argparse
import matplotlib.pyplot as plt
import os
import numpy as np
from models.operating_system import OperatingSystemModel
from utils.reference_generator import generate_random_sequence, generate_locality_sequence, generate_sequential_sequence

def run_simulation(algorithm, num_frames, sequence):
    """Run a simulation with the specified algorithm and number of frames.
    
    Args:
        algorithm: Page replacement algorithm to use (FIFO, LRU, LFU)
        num_frames: Number of physical memory frames available
        sequence: The page reference sequence to use
        
    Returns:
        Dictionary of performance metrics
    """
    os_model = OperatingSystemModel(num_frames=num_frames, page_replacement_algorithm=algorithm)
    metrics = os_model.simulate_page_reference_sequence(sequence)
    
    print(f"\nAlgorithm: {algorithm}, Frames: {num_frames}, Pattern: Sequence Length {len(sequence)}")
    print(f"Page Faults: {metrics['page_faults']}")
    print(f"Hit Rate: {metrics['hit_rate']:.2f}%")
    print(f"Miss Rate: {metrics['miss_rate']:.2f}%")
    
    return metrics

def compare_reference_patterns(algorithms=None, num_frames=8, max_page=16, sequence_length=1000):
    """Compare algorithms across different reference patterns with fixed parameters.
    
    Args:
        algorithms: List of algorithms to test (default: FIFO, LRU, LFU)
        num_frames: Number of physical memory frames (default: 8)
        max_page: Maximum page number (default: 16)
        sequence_length: Length of reference sequences (default: 1000)
        
    Returns:
        Dictionary of results by algorithm and reference pattern
    """
    if algorithms is None:
        algorithms = ["FIFO", "LRU", "LFU"]
    
    # Define reference patterns
    patterns = ["random", "locality", "sequential"]
    
    results = {}
    for algorithm in algorithms:
        results[algorithm] = {}
        print(f"\nRunning comparison for {algorithm} algorithm...")
        
        for pattern in patterns:
            print(f"Simulating pattern: {pattern}")
            if pattern == "random":
                sequence = generate_random_sequence(length=sequence_length, max_page=max_page)
                print(f"Generated random sequence of length {len(sequence)}")
            elif pattern == "locality":
                sequence = generate_locality_sequence(length=sequence_length, max_page=max_page)
                print(f"Generated locality sequence of length {len(sequence)}")
            elif pattern == "sequential":
                sequence = generate_sequential_sequence(length=sequence_length, max_page=max_page)
                print(f"Generated sequential sequence of length {len(sequence)}")
            
            results[algorithm][pattern] = run_simulation(algorithm, num_frames, sequence)
    
    return results

def generate_comparison_charts(results, output_dir="output"):
    """Generate column charts comparing algorithms across reference patterns.
    
    Args:
        results: Dictionary of results by algorithm and reference pattern
        output_dir: Directory to save charts (default: output)
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # Extract algorithms and patterns
    algorithms = list(results.keys())
    patterns = list(results[algorithms[0]].keys())
    
    # Set up the bar chart
    num_algorithms = len(algorithms)
    bar_width = 0.7 / num_algorithms  # Adjust bar width based on number of algorithms
    index = np.arange(len(patterns))
    
    # Plot hit rate comparison
    plt.figure(figsize=(12, 8))
    for i, algorithm in enumerate(algorithms):
        hit_rates = [results[algorithm][pattern]["hit_rate"] for pattern in patterns]
        offset = i - (num_algorithms - 1) / 2  # Center the groups
        plt.bar(index + offset * bar_width, hit_rates, bar_width, label=algorithm)
    
    plt.title("Hit Rate Comparison Across Reference Patterns")
    plt.xlabel("Reference Pattern")
    plt.ylabel("Hit Rate (%)")
    plt.xticks(index, patterns)
    plt.legend()
    plt.grid(True, axis='y')
    plt.savefig(os.path.join(output_dir, "hit_rate_comparison.png"))
    
    # Plot miss rate comparison
    plt.figure(figsize=(12, 8))
    for i, algorithm in enumerate(algorithms):
        miss_rates = [results[algorithm][pattern]["miss_rate"] for pattern in patterns]
        offset = i - (num_algorithms - 1) / 2  # Center the groups
        plt.bar(index + offset * bar_width, miss_rates, bar_width, label=algorithm)
    
    plt.title("Miss Rate Comparison Across Reference Patterns")
    plt.xlabel("Reference Pattern")
    plt.ylabel("Miss Rate (%)")
    plt.xticks(index, patterns)
    plt.legend()
    plt.grid(True, axis='y')
    plt.savefig(os.path.join(output_dir, "miss_rate_comparison.png"))
    
    # Plot page faults comparison
    plt.figure(figsize=(12, 8))
    for i, algorithm in enumerate(algorithms):
        page_faults = [results[algorithm][pattern]["page_faults"] for pattern in patterns]
        offset = i - (num_algorithms - 1) / 2  # Center the groups
        plt.bar(index + offset * bar_width, page_faults, bar_width, label=algorithm)
    
    plt.title("Page Faults Comparison Across Reference Patterns")
    plt.xlabel("Reference Pattern")
    plt.ylabel("Number of Page Faults")
    plt.xticks(index, patterns)
    plt.legend()
    plt.grid(True, axis='y')
    plt.savefig(os.path.join(output_dir, "page_faults_comparison.png"))
    
    print(f"\nComparison charts saved to {output_dir} directory.")

def main():
    """Main function to parse arguments and run simulations."""
    parser = argparse.ArgumentParser(
        description="Run page table replacement algorithm comparisons across reference patterns.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter # Show default values in help
    )
    parser.add_argument("--sweep", action="store_true",
                        help="Run comparison across all algorithms and reference patterns using specified parameters.")
    parser.add_argument("--frames", type=int, default=8,
                        help="Number of physical memory frames available.")
    parser.add_argument("--num-pages", type=int, default=16,
                        help="Number of distinct pages in virtual memory.")
    parser.add_argument("--sequence-length", type=int, default=1000,
                        help="Length of reference sequence for each pattern.")
    parser.add_argument("--output-dir", default="output",
                        help="Directory to save generated charts.")
    
    args = parser.parse_args()
    
    if args.sweep:
        # Run the pattern comparison with specified settings
        print("\n=== Running Algorithm Comparison Across Reference Patterns ===")
        print(f"Settings: {args.frames} frames, {args.num_pages} pages, {args.sequence_length} references")
        results = compare_reference_patterns(
            num_frames=args.frames,
            max_page=args.num_pages,
            sequence_length=args.sequence_length
        )
        # Always generate charts when using --sweep
        generate_comparison_charts(results, args.output_dir)
    else:
        # If --sweep is not provided, print help
        parser.print_help()
        print("\nError: Please use the --sweep flag to run the comparison.")

if __name__ == "__main__":
    main()