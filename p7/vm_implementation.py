class Stack:
    def __init__(self):
        self.stack = []
        self.stack_pointer = -1

    def push(self, value):
        """Pushes value to stack"""
        self.stack_pointer += 1
        self.stack.append(value)

    def pop(self):
        """Pops value from stack if empty"""
        if self.stack_pointer == -1:
            raise Exception("Address out of Bounds")
        self.stack_pointer -= 1
        value = self.stack.pop()
        return value


class MemorySegment:
    def __init__(self, size):
        self.data = [0] * size
        self.size = size

    def read(self, address):
        """
        Read values from memory segments
        """
        if 0 <= address < self.size:
            return self.data[address]
        raise Exception("Address out of Bounds")

    def write(self, address, value):
        """
        Write to memory segments
        """
        if 0 <= address < self.size:
            self.data[address] = value
        else:
            raise Exception("Memory Access Error: Invalid address")


class VM:
    def __init__(self, memory_size=16384):
        self.stack = MemorySegment(size=1024)
        self.local = MemorySegment(size=512)
        self.argument = MemorySegment(size=512)
        self.static = MemorySegment(size=256)
        self.constant = MemorySegment(size=256)

        self.stack_obj = Stack()

        self.local_base = 0
        self.argument_base = 0
        self.static_base = 0
        self.this_base = 0
        self.that_base = 0
        self.pointer_base = 0
        self.temp_base = 0

        self.segment_bases = {
                "local" : self.local_base,
                "argument" : self.argument_base,
                "static" : self.static_base,
                "this" : self.this_base,
                "that" : self.that_base,
                "pointer" : self.pointer_base,
                "temp" : self.pointer_base,
        }

    def get_segment(self,segment_name):
        if segment_name == "local":
            return self.local
        elif segment_name == "argument":
            return self.argument
        elif segment_name == "static":
            return self.static 
        elif segment_name == "this":  
            return self.this
        elif segment_name == "that":
            return self.that
        elif segment_name == "pointer":
            return self.pointer
        elif segment_name == "temp":
            return self.temp
        else:
            raise ValueError(f"Invalid segment name: {segment_name}") 

    def execute_program(self, program):
        self.pc = 0
        self.labels = self.process_labels(program)

        while self.pc < len(program):
            instruction = program[self.pc]
            instruction_type, arg1, arg2 = self.parse_instruction(instruction)
            self.execute_instruction(instruction, arg1, arg2)
            if instruction_type not in ["goto", "if-goto"]:
                self.pc += 1

    def process_labels(program):
        labels = {}
        address = 0
        for instruction in program:
            instruction_type, arg1, arg2 = self.parse_instruction(instruction)
            if instruction_type == "label":
                labels_name = arg1
                labels[labels_name] = address
            else:
                address += 1
        return labels

    def parse_instruction(self, instruction):
        """Parses a single VM instruction line
        Args:
            instruction(str):  Single VM instruction
        Returns:
            tuple: formatted as (instruction_type,arg1,arg2)
        """
        tokens = instruction.strip().split()
        instruction_type = tokens[0] if tokens else None
        arg1 = tokens[1] if len(tokens) > 1 else None
        arg2 = tokens[2] if len(tokens) > 2 else None
        return instruction_type, arg1, arg2


    def execute_instruction(self, instruction_type, arg1=None, arg2=None):
        if instruction_type == "add":
            if self.stack_obj.stack_pointer < 1:
                raise Exception("Stack underflow: Cannot add on empty stack")
            operand2 = self.stack_obj.pop()
            operand1 = self.stack_obj.pop()
            result = operand2 + operand1
            self.stack_obj.push(result)

        elif instruction_type == "sub":
            if self.stack_obj.stack_pointer < 1:
                raise Exception("Stack underflow: Cannot sub on empty stack")
            operand2 = self.stack_obj.pop()
            operand1 = self.stack_obj.pop()
            result = operand1 - operand2
            self.stack_obj.push(result)

        elif instruction_type == "neg":
            if self.stack_obj.stack_pointer < 0:
                raise Exception("Stack Underflow")
            operand = self.stack_obj.pop()
            result = -1 * operand
            self.stack_obj.push(result)

        elif instruction_type == "gt":
            if self.stack_obj.stack_pointer < 1:
                raise Exception("Stack Underflow: Cant compare empty stack")
            operand2 = self.stack_obj.pop()
            operand1 = self.stack_obj.pop()
            result = operand1 > operand2
            self.stack_obj.push(result)

        elif instruction_type == "lt":
            if self.stack_obj.stack_pointer < 1:
                raise Exception("Stack Underflow: Cant compare empty stack")
            operand2 = self.stack_obj.pop()
            operand1 = self.stack_obj.pop()
            result = operand1 < operand2
            self.stack_obj.push(result)

        elif instruction_type == "eq":
            if self.stack_obj.stack_pointer < 1:
                raise Exception("Stack Underflow: Cant compare empty stack")
            operand2 = self.stack_obj.pop()
            operand1 = self.stack_obj.pop()
            result = operand1 == operand2
            self.stack_obj.push(result)

        elif instruction_type == "and":
            if self.stack_obj.stack_pointer < 1:
                raise Exception("Stack Underflow: Cant compare empty stack")
            operand2 = self.stack_obj.pop()
            operand1 = self.stack_obj.pop()
            result = operand1 and operand2
            self.stack_obj.push(result)

        elif instruction_type == "or":
            if self.stack_obj.stack_pointer < 1:
                raise Exception("Stack Underflow: Cant compare empty stack")
            operand2 = self.stack_obj.pop()
            operand1 = self.stack_obj.pop()
            result = operand1 or operand2
            self.stack_obj.push(result)

        elif instruction_type == "not":
            if self.stack_obj.stack_pointer < 0:
                raise Exception("Stack Underflow: Cant compare empty stack")
            operand = self.stack_obj.pop()
            result = not operand
            self.stack_obj.push(result)
        
        elif instruction_type == "push":
            segment = arg1
            index = int(arg2)
            segment_address = self.segment_bases[segment] + index

            if segment == "constant":
                value = index
            else: 
                value = self.get_segment(segment).read(segment_address)
            self.stack_obj.push(value)

        elif instruction_type == "pop":
            if self.stack_obj.stack_pointer < 0:  
                raise Exception("Stack underflow error ")

            segment = arg1
            index = int(arg2)
            segment_address = self.segment_bases[segment] + index
            value = self.stack_obj.pop()
            self.get_segment(segment).write(segment_address, value)

        elif instruction_type == "goto":
            label_to_jump_to = arg1
            self.pc = self.labels.get(label_to_jump_to)
            if self.pc is None:
                raise Exception(f"invalid label: {label_to_jump_to}")

        elif instruction_type == "if-goto":
            label_to_jump_to = arg1
            condition = self.stack_obj.pop()
            if condition != 0:
                self.pc = self.labels.get(label_to_jump_to)
                if self.pc is None:
                    raise Exception(f"invalid label: {label_to_jump_to}")

        elif instruction_type == "call":
            function_name = arg1
            num_args = int(arg2)

            #Push return address onto the stack
            return_address = self.pc + 1  # Address of the instruction AFTER 'call'
            self.stack_obj.push(return_address)

            # Push state (base pointers) onto the stack
            self.stack_obj.push(self.local_base)
            self.stack_obj.push(self.argument_base)
            self.stack_obj.push(self.this_base)
            self.stack_obj.push(self.that_base)

            # Set new 'argument_base'
            self.argument_base = self.stack_obj.stack_pointer - num_args - 4  # Adjust for pushed values

            # Set new 'local_base'
            self.local_base = self.argument_base - 1 

            # Jump to the function's code 
            self.pc = self.labels.get(function_name)
            if self.pc is None:
                raise ValueError(f"Invalid function name: {function_name}")

        elif instruction_type == "return":
            # Get the return value (if any)
            return_value = self.stack_obj.pop()  # Assuming the function left the return value on top of the stack

            # Restore the caller's stack frame
            self.that_base = self.stack_obj.pop()
            self.this_base = self.stack_obj.pop()
            self.argument_base = self.stack_obj.pop()
            self.local_base = self.stack_obj.pop()

            # Position stack for the return value
            self.stack_obj.stack_pointer = self.argument_base  

            # Push the return value back onto the stack (if needed)
            self.stack_obj.push(return_value)  

            # Retrieve the return address
            return_address = self.stack_obj.pop()

            #  Jump back to the caller
            self.pc = return_address

