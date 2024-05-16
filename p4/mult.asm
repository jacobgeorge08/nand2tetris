@R0
D=M

@ZERO
D; JLE

@n // Setting n to hold value of R0
M=D

@inter //Setting intermediary value to 0
M=0

(LOOP)
@R1
D=M

@ZERO
D; JLE

@inter
M=M+D

@n
MD = M-1

@LOOP
D; JGT

@inter
D=M

@R2
M=D

(END)
@END
0 ; JMP

(ZERO)
@R2
M=0

@END
0 ; JMP 
