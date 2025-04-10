import pytest
from utils.process_generator import generate_instructions, create_process
from models.process import INSTRUCTION_COSTS

def test_generate_instructions_all_cpu():
    """Test that generate_instructions produces only CPU instructions when probability is 1.0"""
    num_instructions = 100
    cpu_probability = 1.0
    instructions = generate_instructions(num_instructions, cpu_probability)
    
    assert len(instructions) == num_instructions
    # All instructions should be CPU instructions
    cpu_instructions = ['ADD', 'SUB', 'MUL', 'DIV']
    for instr in instructions:
        assert instr in cpu_instructions

def test_generate_instructions_all_memory():
    """Test that generate_instructions produces only memory instructions when probability is 0.0"""
    num_instructions = 100
    cpu_probability = 0.0
    instructions = generate_instructions(num_instructions, cpu_probability)
    
    assert len(instructions) == num_instructions
    # All instructions should be memory instructions
    memory_instructions = ['LOAD', 'STORE']
    for instr in instructions:
        assert instr in memory_instructions

def test_generate_instructions_mixed():
    """Test that generate_instructions produces a mix of instructions with probability 0.5"""
    num_instructions = 1000  # Large enough for statistical significance
    cpu_probability = 0.5
    instructions = generate_instructions(num_instructions, cpu_probability)
    
    assert len(instructions) == num_instructions
    
    # Count CPU and memory instructions
    cpu_count = 0
    memory_count = 0
    cpu_instructions = ['ADD', 'SUB', 'MUL', 'DIV']
    memory_instructions = ['LOAD', 'STORE']
    
    for instr in instructions:
        if instr in cpu_instructions:
            cpu_count += 1
        elif instr in memory_instructions:
            memory_count += 1
    
    # We expect roughly equal numbers, but allow for some random variation
    assert cpu_count > 0
    assert memory_count > 0
    # The counts should be roughly equal with 0.5 probability (within 20% of expected)
    assert abs(cpu_count - num_instructions/2) < num_instructions * 0.2

def test_create_process():
    """Test that create_process correctly creates a Process instance"""
    process_id = 42
    num_instructions = 10
    cpu_probability = 0.7
    
    process = create_process(process_id, num_instructions, cpu_probability)
    
    assert process.process_id == process_id
    assert len(process.instructions) == num_instructions
    assert process.pc == 0  # Program counter starts at 0 