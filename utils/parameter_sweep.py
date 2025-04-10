import os
import numpy as np
import matplotlib.pyplot as plt
from models.operating_system import OperatingSystemModel
from utils.process_generator import create_process
from models.scheduler import fcfs_scheduler, round_robin_scheduler

def perform_parameter_sweep():
    """
    Perform parameter sweeps for CPU probability and quantum.
    Generate and save charts of the results.
    """
    # Ensure output directory exists
    os.makedirs('output', exist_ok=True)
    
    # Define parameter sweep ranges
    cpu_probabilities = np.arange(0, 1, 0.1)
    quanta = np.arange(100, 1000, 100)
    num_processes = 16
    num_instructions = 32000 
    
    # Data structures to store results
    fcfs_results = []
    rr_results = {quantum: [] for quantum in quanta}
    
    # Run FCFS simulations for different CPU probabilities
    print("Running FCFS simulations...")
    for cpu_prob in cpu_probabilities:
        print(f"[FCFS] Starting simulation for cpu_probability = {cpu_prob:.1f}")
        metrics = run_simulation(cpu_prob, 500, scheduler_type='fcfs', num_processes=num_processes, num_instructions=num_instructions)  # Quantum doesn't matter for FCFS
        print(f"[FCFS] Finished simulation for cpu_probability = {cpu_prob:.1f}; Total time: {metrics['total_time']} ns")
        fcfs_results.append(metrics)
    
    # Run RR simulations for different CPU probabilities and quanta
    print("Running Round Robin simulations...")
    for quantum in quanta:
        for cpu_prob in cpu_probabilities:
            print(f"[RR] Starting simulation for quantum = {quantum} ns, cpu_probability = {cpu_prob:.1f}")
            metrics = run_simulation(cpu_prob, quantum, scheduler_type='rr', num_processes=num_processes, num_instructions=num_instructions)
            print(f"[RR] Finished simulation for quantum = {quantum} ns, cpu_probability = {cpu_prob:.1f}; Total time: {metrics['total_time']} ns")
            rr_results[quantum].append(metrics)
    
    # Generate charts
    generate_charts(cpu_probabilities, quanta, fcfs_results, rr_results)

def run_simulation(cpu_probability, quantum, num_processes=4, num_instructions=20, scheduler_type='rr'):
    """
    Run a single simulation with the given parameters.
    
    Args:
        cpu_probability: Probability of generating CPU instructions
        quantum: Time quantum for Round Robin scheduling (ignored for FCFS)
        num_processes: Number of processes to simulate
        num_instructions: Number of instructions per process
        scheduler_type: 'fcfs' or 'rr' for the scheduler algorithm
    
    Returns:
        Dictionary with performance metrics
    """
    # Initialize the OS model with the specified quantum
    os_model = OperatingSystemModel(quantum=quantum)
    
    # Create processes
    processes = {}
    for i in range(1, num_processes + 1):
        proc = create_process(i, num_instructions, cpu_probability)
        processes[i] = proc
        os_model.add_process(i, "PR_READY", os_model.current_time)
    
    # Run the appropriate scheduler
    if scheduler_type == 'fcfs':
        fcfs_scheduler(os_model, processes)
    else:
        round_robin_scheduler(os_model, processes)
    
    # Collect metrics
    metrics = {
        'total_time': os_model.current_time,
        'processes': []
    }
    
    for entry in os_model.process_table:
        turnaround_time = entry.end_time - entry.start_time
        waiting_time = turnaround_time - entry.cpu_time
        metrics['processes'].append({
            'process_id': entry.process_id,
            'turnaround_time': turnaround_time,
            'cpu_time': entry.cpu_time,
            'waiting_time': waiting_time
        })
    
    return metrics

def generate_charts(cpu_probabilities, quanta, fcfs_results, rr_results):
    """
    Generate and save charts of the simulation results.
    
    Args:
        cpu_probabilities: List of CPU probability values
        quanta: List of quantum values for RR
        fcfs_results: List of FCFS simulation results
        rr_results: Dictionary mapping quantum values to lists of RR simulation results
    """
    # --- CPU Probability Impact Charts ---
    
    # 1. Total Simulation Time vs CPU Probability for all schedulers
    plt.figure(figsize=(10, 6))
    
    # Plot FCFS
    fcfs_total_times = [result['total_time'] for result in fcfs_results]
    plt.plot(cpu_probabilities, fcfs_total_times, 'o-', label='FCFS')
    
    # Plot RR with different quanta
    for quantum in quanta:
        rr_total_times = [result['total_time'] for result in rr_results[quantum]]
        plt.plot(cpu_probabilities, rr_total_times, 'o-', label=f'RR (Q={quantum})')
    
    plt.xlabel('CPU Instruction Probability')
    plt.ylabel('Total Simulation Time (ns)')
    plt.title('Impact of CPU Instruction Probability on Total Simulation Time')
    plt.legend()
    plt.grid(True)
    plt.savefig('output/total_time_vs_cpu_prob.png', dpi=300, bbox_inches='tight')
    
    # 2. Average Turnaround Time vs CPU Probability
    plt.figure(figsize=(10, 6))
    
    # Plot FCFS
    fcfs_avg_turnaround = [np.mean([p['turnaround_time'] for p in result['processes']]) for result in fcfs_results]
    plt.plot(cpu_probabilities, fcfs_avg_turnaround, 'o-', label='FCFS')
    
    # Plot RR with different quanta
    for quantum in quanta:
        rr_avg_turnaround = [np.mean([p['turnaround_time'] for p in result['processes']]) for result in rr_results[quantum]]
        plt.plot(cpu_probabilities, rr_avg_turnaround, 'o-', label=f'RR (Q={quantum})')
    
    plt.xlabel('CPU Instruction Probability')
    plt.ylabel('Average Turnaround Time (ns)')
    plt.title('Impact of CPU Instruction Probability on Average Turnaround Time')
    plt.legend()
    plt.grid(True)
    plt.savefig('output/avg_turnaround_vs_cpu_prob.png', dpi=300, bbox_inches='tight')
    
    # 3. Average Waiting Time vs CPU Probability
    plt.figure(figsize=(10, 6))
    
    # Plot FCFS
    fcfs_avg_waiting = [np.mean([p['waiting_time'] for p in result['processes']]) for result in fcfs_results]
    plt.plot(cpu_probabilities, fcfs_avg_waiting, 'o-', label='FCFS')
    
    # Plot RR with different quanta
    for quantum in quanta:
        rr_avg_waiting = [np.mean([p['waiting_time'] for p in result['processes']]) for result in rr_results[quantum]]
        plt.plot(cpu_probabilities, rr_avg_waiting, 'o-', label=f'RR (Q={quantum})')
    
    plt.xlabel('CPU Instruction Probability')
    plt.ylabel('Average Waiting Time (ns)')
    plt.title('Impact of CPU Instruction Probability on Average Waiting Time')
    plt.legend()
    plt.grid(True)
    plt.savefig('output/avg_waiting_vs_cpu_prob.png', dpi=300, bbox_inches='tight')
    
    # --- Quantum Impact Charts (for RR only) ---
    
    # 4. Total Simulation Time vs Quantum for different CPU probabilities
    plt.figure(figsize=(10, 6))
    
    for i, cpu_prob in enumerate(cpu_probabilities):
        total_times = [rr_results[quantum][i]['total_time'] for quantum in quanta]
        plt.plot(quanta, total_times, 'o-', label=f'CPU Prob={cpu_prob:.1f}')
    
    plt.xlabel('Round Robin Quantum (ns)')
    plt.ylabel('Total Simulation Time (ns)')
    plt.title('Impact of Round Robin Quantum on Total Simulation Time')
    plt.legend()
    plt.grid(True)
    plt.savefig('output/total_time_vs_quantum.png', dpi=300, bbox_inches='tight')
    
    # 5. Average Turnaround Time vs Quantum
    plt.figure(figsize=(10, 6))
    
    for i, cpu_prob in enumerate(cpu_probabilities):
        avg_turnaround = [np.mean([p['turnaround_time'] for p in rr_results[quantum][i]['processes']]) for quantum in quanta]
        plt.plot(quanta, avg_turnaround, 'o-', label=f'CPU Prob={cpu_prob:.1f}')
    
    plt.xlabel('Round Robin Quantum (ns)')
    plt.ylabel('Average Turnaround Time (ns)')
    plt.title('Impact of Round Robin Quantum on Average Turnaround Time')
    plt.legend()
    plt.grid(True)
    plt.savefig('output/avg_turnaround_vs_quantum.png', dpi=300, bbox_inches='tight')
    
    # 6. Average Waiting Time vs Quantum
    plt.figure(figsize=(10, 6))
    
    for i, cpu_prob in enumerate(cpu_probabilities):
        avg_waiting = [np.mean([p['waiting_time'] for p in rr_results[quantum][i]['processes']]) for quantum in quanta]
        plt.plot(quanta, avg_waiting, 'o-', label=f'CPU Prob={cpu_prob:.1f}')
    
    plt.xlabel('Round Robin Quantum (ns)')
    plt.ylabel('Average Waiting Time (ns)')
    plt.title('Impact of Round Robin Quantum on Average Waiting Time')
    plt.legend()
    plt.grid(True)
    plt.savefig('output/avg_waiting_vs_quantum.png', dpi=300, bbox_inches='tight')
    
    # Create a heatmap of avg turnaround time for RR
    plt.figure(figsize=(10, 6))
    heatmap_data = np.zeros((len(cpu_probabilities), len(quanta)))
    
    for i, cpu_prob in enumerate(cpu_probabilities):
        for j, quantum in enumerate(quanta):
            avg_turnaround = np.mean([p['turnaround_time'] for p in rr_results[quantum][i]['processes']])
            heatmap_data[i, j] = avg_turnaround
    
    plt.imshow(heatmap_data, cmap='hot', aspect='auto', origin='lower')
    plt.colorbar(label='Average Turnaround Time (ns)')
    
    # Set x and y tick labels
    plt.xticks(np.arange(len(quanta)), [f'{q}' for q in quanta])
    plt.yticks(np.arange(len(cpu_probabilities)), [f'{p:.1f}' for p in cpu_probabilities])
    
    plt.xlabel('Round Robin Quantum (ns)')
    plt.ylabel('CPU Instruction Probability')
    plt.title('Heatmap of Average Turnaround Time')
    plt.savefig('output/turnaround_heatmap.png', dpi=300, bbox_inches='tight')
    
    print("Charts have been generated and saved to the 'output' directory.") 