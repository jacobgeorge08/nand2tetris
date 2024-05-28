jmp_dict = {"null" : "000",
            "JGT" : "001",
            "JEQ" : "010",
            "JGE" : "011",
            "JLT" : "100",
            "JNE" : "101",
            "JLE" : "110",
            "JMP" : "111"}

dest_dict = {"null" : "000",
            "M" : "001",
            "D" : "010",
            "MD" : "011",
            "A" : "100",
            "AM" : "101",
            "AD" : "110",
            "AMD" : "111"}

comp_dict = {
    '0': '101010',
    '1': '111111',
    '-1': '111010',
    'D': '001100',
    'A': '110000',
    '!D': '001101',
    '!A': '110001',
    'D+1': '011111',
    '-A': '110011',
    '-D': '001111',
    'A+1': '110111',
    'A-1': '110010',
    'A-D': '000111',
    'D+A': '000010',
    'D-A': '100111',
    'D-1': '010011',
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
    'D|M': '010101',
}


hack_inst = [] 

with open('hack_files/RectL.asm', 'r') as file:
    file_contents = file.read()
    hack_input = file_contents.split('\n')
    hack_inst = [line.strip() for line in hack_input if line.strip() != '' and not line.strip().startswith("//")]

asm_inst = hack_inst

for i in range(len(hack_inst)):
    comp_str = '0'
    comp_bin,jmp_bin,dest_bin = '101010', '000', '000' 
    a_bit = "0"

    if hack_inst[i][0] == '@':
        addr = int(hack_inst[i][1:])
        bin_addr = format(addr,'016b')
        a_reg = bin_addr
        asm_inst[i] = bin_addr
    
    else:
        if ';' in hack_inst[i]:
            jmp_str = hack_inst[i][hack_inst[i].find(';') + 1:]
            jmp_bin = jmp_dict[jmp_str]
            comp_str = hack_inst[i][:hack_inst[i].find(';')]
            comp_bin = comp_dict[comp_str]

        elif '=' in hack_inst[i]:
            dest_str = hack_inst[i][:hack_inst[i].find('=')]
            dest_bin = dest_dict[dest_str]        
            comp_str = hack_inst[i][hack_inst[i].find('=') + 1:]
            comp_bin = comp_dict[comp_str]

        if comp_str.find('M') != - 1:
            a_bit = "1"

        c_inst = '111' + a_bit +comp_bin + dest_bin + jmp_bin
        asm_inst[i] = c_inst

asm = "\n".join(asm_inst)
print(asm)

