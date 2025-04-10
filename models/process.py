# Define instruction execution times in ns
INSTRUCTION_COSTS = {
    'LOAD': 10,
    'STORE': 20,
    'ADD': 1,
    'SUB': 1,
    'MUL': 5,
    'DIV': 5
}

class Process:
    def __init__(self, process_id, instructions):
        """
        Initialize a process with an id and a list of instructions.
        :param process_id: Unique identifier for the process.
        :param instructions: List of instructions (strings) to execute.
        """
        self.process_id = process_id
        self.instructions = instructions
        self.pc = 0  # Program counter

    def is_finished(self):
        """Return True if all instructions have been executed."""
        return self.pc >= len(self.instructions)

    def peek_next_instruction_cost(self):
        """
        Peek at the cost of the next instruction.
        Returns 0 if finished or instruction not recognized.
        """
        if self.is_finished():
            return 0
        instr = self.instructions[self.pc].strip()
        return INSTRUCTION_COSTS.get(instr, 0)

    def execute_next_instruction(self):
        """
        Execute the next instruction and return its cost.
        Advances the program counter.
        """
        if self.is_finished():
            return 0
        cost = self.peek_next_instruction_cost()
        self.pc += 1
        return cost 