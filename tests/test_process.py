import pytest
from models.process import Process, INSTRUCTION_COSTS

def test_is_finished_empty():
    p = Process(1, [])
    assert p.is_finished() is True

def test_is_finished_after_execution():
    instructions = ["LOAD", "ADD"]
    p = Process(1, instructions)
    assert p.is_finished() is False
    p.execute_next_instruction()  # Executes "LOAD"
    assert p.is_finished() is False
    p.execute_next_instruction()  # Executes "ADD"
    assert p.is_finished() is True

def test_peek_next_instruction_cost_known():
    instructions = ["LOAD", "INVALID"]
    p = Process(1, instructions)
    cost = p.peek_next_instruction_cost()
    assert cost == INSTRUCTION_COSTS["LOAD"]

def test_peek_next_instruction_cost_unknown():
    instructions = ["FOO"]
    p = Process(1, instructions)
    cost = p.peek_next_instruction_cost()
    assert cost == 0

def test_execute_next_instruction():
    instructions = ["LOAD", "ADD", "STORE"]
    p = Process(1, instructions)
    cost1 = p.execute_next_instruction()
    assert cost1 == INSTRUCTION_COSTS["LOAD"]
    cost2 = p.execute_next_instruction()
    assert cost2 == INSTRUCTION_COSTS["ADD"]
    cost3 = p.execute_next_instruction()
    assert cost3 == INSTRUCTION_COSTS["STORE"]
    # Now the process should be finished so further execution returns 0.
    cost4 = p.execute_next_instruction()
    assert cost4 == 0 