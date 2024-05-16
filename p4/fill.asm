@color // default value of color is set to white  
M=0

(LOOP)
    @SCREEN
    D=A 
    @addr //Setting address to inital value of screen that we need to iter over 
    M=D 

    @KBD // Looking for keyb input
    D=M 

    @BLACK // jump to black if there is keyb input 
    D; JGT 

    @color
    M=0
    @COLOR_SCREEN // unconditional jump to screen coloring
    0; JMP

    (BLACK)
        @color
        M=-1

    (COLOR_SCREEN)
        @color
        D=M 
        @addr 
        A=M // The A register is set as address stored in addr
        M=D // value of A register is set to value of color

        @addr // current address is incremented
        DM=M+1
        
        @24576 // SCREEN ADDRESS (16384) + (256 * 512) / 16
        D=D-A
        @COLOR_SCREEN
        D; JLT

@LOOP // infinite loop
0; JMP
