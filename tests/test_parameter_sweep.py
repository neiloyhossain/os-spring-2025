import pytest
import os
import numpy as np
from unittest.mock import patch, MagicMock
from utils.parameter_sweep import run_simulation, perform_parameter_sweep, generate_charts

def test_run_simulation():
    """Test that run_simulation correctly runs a simulation and returns metrics"""
    # Run a simple simulation with predictable parameters
    cpu_probability = 0.5
    quantum = 200
    num_processes = 2
    num_instructions = 5
    
    # Run the simulation
    metrics = run_simulation(
        cpu_probability=cpu_probability,
        quantum=quantum,
        num_processes=num_processes,
        num_instructions=num_instructions,
        scheduler_type='fcfs'
    )
    
    # Verify the structure of the returned metrics
    assert 'total_time' in metrics
    assert 'processes' in metrics
    assert len(metrics['processes']) == num_processes
    
    # Check process metrics structure
    for proc_metrics in metrics['processes']:
        assert 'process_id' in proc_metrics
        assert 'turnaround_time' in proc_metrics
        assert 'cpu_time' in proc_metrics
        assert 'waiting_time' in proc_metrics
        
        # Basic sanity checks
        assert proc_metrics['turnaround_time'] >= proc_metrics['cpu_time']
        assert proc_metrics['waiting_time'] == proc_metrics['turnaround_time'] - proc_metrics['cpu_time']

@patch('utils.parameter_sweep.generate_charts')
@patch('utils.parameter_sweep.run_simulation')
def test_perform_parameter_sweep(mock_run_simulation, mock_generate_charts):
    """Test that perform_parameter_sweep correctly runs simulations with different parameters"""
    # Mock the run_simulation function to return a simple metrics dict
    mock_metrics = {
        'total_time': 1000,
        'processes': [
            {'process_id': 1, 'turnaround_time': 1000, 'cpu_time': 500, 'waiting_time': 500}
        ]
    }
    mock_run_simulation.return_value = mock_metrics
    
    # Mock os.makedirs
    with patch('os.makedirs') as mock_makedirs:
        # Run the parameter sweep
        perform_parameter_sweep()
        
        # Verify that the output directory was created
        mock_makedirs.assert_called_once_with('output', exist_ok=True)
        
        # Verify that run_simulation was called at least once
        assert mock_run_simulation.call_count > 0
        
        # Verify that generate_charts was called once
        assert mock_generate_charts.call_count == 1

@patch('matplotlib.pyplot.savefig')
@patch('matplotlib.pyplot.figure')
def test_generate_charts(mock_figure, mock_savefig):
    """Test that generate_charts correctly generates and saves charts"""
    # Create sample data
    cpu_probabilities = np.array([0.0, 0.5, 1.0])
    quanta = np.array([100, 500, 1000])
    
    # Create sample metrics
    fcfs_results = [
        {'total_time': 1000, 'processes': [{'turnaround_time': 1000, 'cpu_time': 500, 'waiting_time': 500}]},
        {'total_time': 800, 'processes': [{'turnaround_time': 800, 'cpu_time': 400, 'waiting_time': 400}]},
        {'total_time': 600, 'processes': [{'turnaround_time': 600, 'cpu_time': 300, 'waiting_time': 300}]}
    ]
    
    rr_results = {
        100: [
            {'total_time': 1100, 'processes': [{'turnaround_time': 1100, 'cpu_time': 550, 'waiting_time': 550}]},
            {'total_time': 900, 'processes': [{'turnaround_time': 900, 'cpu_time': 450, 'waiting_time': 450}]},
            {'total_time': 700, 'processes': [{'turnaround_time': 700, 'cpu_time': 350, 'waiting_time': 350}]}
        ],
        500: [
            {'total_time': 1050, 'processes': [{'turnaround_time': 1050, 'cpu_time': 525, 'waiting_time': 525}]},
            {'total_time': 850, 'processes': [{'turnaround_time': 850, 'cpu_time': 425, 'waiting_time': 425}]},
            {'total_time': 650, 'processes': [{'turnaround_time': 650, 'cpu_time': 325, 'waiting_time': 325}]}
        ],
        1000: [
            {'total_time': 1000, 'processes': [{'turnaround_time': 1000, 'cpu_time': 500, 'waiting_time': 500}]},
            {'total_time': 800, 'processes': [{'turnaround_time': 800, 'cpu_time': 400, 'waiting_time': 400}]},
            {'total_time': 600, 'processes': [{'turnaround_time': 600, 'cpu_time': 300, 'waiting_time': 300}]}
        ]
    }
    
    # Call generate_charts
    generate_charts(cpu_probabilities, quanta, fcfs_results, rr_results)
    
    # Verify that all the expected charts were generated
    assert mock_figure.call_count >= 6  # At least 6 charts
    assert mock_savefig.call_count >= 6  # At least 6 saved files
    
    # Verify that charts were saved to the output directory
    expected_files = [
        'output/total_time_vs_cpu_prob.png',
        'output/avg_turnaround_vs_cpu_prob.png',
        'output/avg_waiting_vs_cpu_prob.png',
        'output/total_time_vs_quantum.png',
        'output/avg_turnaround_vs_quantum.png',
        'output/avg_waiting_vs_quantum.png',
        'output/turnaround_heatmap.png'
    ]
    
    # Check that each expected file was saved
    for file_path in expected_files:
        assert any(call.args[0] == file_path for call in mock_savefig.call_args_list) 