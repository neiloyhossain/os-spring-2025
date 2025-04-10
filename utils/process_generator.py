import random
from models.process import Process, INSTRUCTION_COSTS

def generate_instructions(num_instructions, cpu_probability):
    """
    Generate a list of instructions based on the probability of CPU vs memory instructions.
    
    Args:
        num_instructions: Number of instructions to generate
        cpu_probability: Probability of generating a CPU instruction (0.0 to 1.0)
                         Higher values mean more CPU-intensive workload
    
    Returns:
        A list of instructions as strings
    """
    instructions = []
    
    # Define CPU and memory instruction types
    cpu_instructions = ['ADD', 'SUB', 'MUL', 'DIV']
    memory_instructions = ['LOAD', 'STORE']
    
    for _ in range(num_instructions):
        # Decide whether to generate a CPU or memory instruction
        if random.random() < cpu_probability:
            # Generate a CPU instruction
            instructions.append(random.choice(cpu_instructions))
        else:
            # Generate a memory instruction
            instructions.append(random.choice(memory_instructions))
    
    return instructions

def create_process(process_id, num_instructions, cpu_probability):
    """
    Create a process with instructions generated based on the given CPU probability.
    
    Args:
        process_id: Unique ID for the process
        num_instructions: Number of instructions to generate
        cpu_probability: Probability of generating CPU instructions (0.0 to 1.0)
    
    Returns:
        A Process instance with the generated instructions
    """
    instructions = generate_instructions(num_instructions, cpu_probability)
    return Process(process_id, instructions) 