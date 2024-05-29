jmp_dict = {
    "null": "000",
    "JGT": "001",
    "JEQ": "010",
    "JGE": "011",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111"
}

dest_dict = {
    "null": "000",
    "M": "001",
    "D": "010",
    "MD": "011",
    "A": "100",
    "AM": "101",
    "AD": "110",
    "AMD": "111"
}

comp_dict = {
    '0': '101010',
    '1': '111111',
    '-1': '111010',
    'D': '001100',
    'A': '110000',
    '!D': '001101',
    '!A': '110001',
    '-D': '001111',
    '-A': '110011',
    'D+1': '011111',
    'A+1': '110111',
    'D-1': '000111',
    'A-1': '110010',
    'D+A': '000010',
    'D-A': '010011',
    'A-D': '000111',
    'D&A': '000000',
    'D|A': '010101',
    'M': '110000',
    '!M': '110001',
    '-M': '110011',
    'M+1': '110111',
    'M-1': '110010',
    'D+M': '000010',
    'D-M': '010011',
    'M-D': '000111',
    'D&M': '000000',
    'D|M': '010101'
}

symbol_table = {
    'SCREEN': 16384,
    'KBD': 24576,
    'SP': 0,
    'LCL': 1,
    'ARG': 2,
    'THIS': 3,
    'THAT': 4,
    'R0': 0,
    'R1': 1,
    'R2': 2,
    'R3': 3,
    'R4': 4,
    'R5': 5,
    'R6': 6,
    'R7': 7,
    'R8': 8,
    'R9': 9,
    'R10': 10,
    'R11': 11,
    'R12': 12,
    'R13': 13,
    'R14': 14,
    'R15': 15,
}

next_avail_addr = 16

# Function to add a new symbol
def add_symbol(symbol, address):
    global next_avail_addr
    if symbol not in symbol_table:
        symbol_table[symbol] = address
        next_avail_addr += 1

# Reading asm file
hack_inst = [] 
with open('hack_files/Rect.asm', 'r') as file:
    file_contents = file.read()
    hack_input = file_contents.split('\n')
    hack_inst = [line.strip() for line in hack_input if line.strip() != '' and not line.strip().startswith("//")]

# First pass to add label symbols
def first_pass():
    current_address = 0
    for line in hack_inst:
        if line.startswith('(') and line.endswith(')'):
            symbol = line[1:-1]
            symbol_table[symbol] = current_address
        else:
            current_address += 1

# Second pass to translate instructions
def second_pass():
    asm_inst = []
    global next_avail_addr
    for line in hack_inst:
        if line.startswith('@'):
            symbol = line[1:]
            if symbol.isdigit():
                address = int(symbol)
            else:
                if symbol not in symbol_table:
                    symbol_table[symbol] = next_avail_addr
                    next_avail_addr += 1
                address = symbol_table[symbol]
            bin_addr = format(address, '016b')
            asm_inst.append(bin_addr)
        elif not line.startswith('(') and not line.endswith(')'):
            dest_bin = '000'
            comp_bin = '101010'
            jmp_bin = '000'
            a_bit = '0'
            if '=' in line:
                dest_str, rest = line.split('=')
                dest_bin = dest_dict[dest_str]
                comp_str = rest
            else:
                rest = line
            if ';' in rest:
                comp_str, jmp_str = rest.split(';')
                jmp_bin = jmp_dict[jmp_str]
            else:
                comp_str = rest
            if 'M' in comp_str:
                a_bit = '1'
            comp_bin = comp_dict[comp_str]
            c_inst = '111' + a_bit + comp_bin + dest_bin + jmp_bin
            asm_inst.append(c_inst)
    return asm_inst

first_pass()
binary_code = second_pass()
asm = "\n".join(binary_code)
print(asm)
