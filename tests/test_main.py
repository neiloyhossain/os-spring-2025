import sys
import pytest
from models.process import Process
import main

def dummy_load_process(file_path, process_id):
    # Always return a process with the same known instructions.
    return Process(process_id, ["LOAD", "ADD", "STORE"])

# Automatically patch main.load_process to avoid I/O in tests.
@pytest.fixture(autouse=True)
def patch_load_process(monkeypatch):
    monkeypatch.setattr(main, "load_process", dummy_load_process)

def run_main_with_args(args, capsys):
    original_argv = sys.argv
    sys.argv = args
    try:
        main.main()
        captured = capsys.readouterr().out
    finally:
        sys.argv = original_argv
    return captured

def test_main_fcfs(capsys):
    # Test main with the FCFS scheduler.
    output = run_main_with_args(["main.py", "--scheduler", "fcfs"], capsys)
    assert "Running FCFS scheduler..." in output
    assert "Process Metrics:" in output
    assert "Total simulation time:" in output

def test_main_rr(capsys):
    # Test main with the Round Robin scheduler.
    output = run_main_with_args(["main.py", "--scheduler", "rr"], capsys)
    assert "Running Round Robin scheduler..." in output
    assert "Process Metrics:" in output
    assert "Total simulation time:" in output 