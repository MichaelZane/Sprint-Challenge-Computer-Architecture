"""CPU functionality."""

import sys

#Binary op codes | base 10

LDI = 0b10000010    #130
PRN = 0b01000111    #71
HLT = 0b00000001    #1
MUL = 0b10100010    #130
PUSH = 0b01000101   #69
POP = 0b01000110    #70
CALL = 0b01010000   #80
RET = 0b00010001    #17
ADD = 0b10100000    #160
CMP = 0b10100111    #167
JMP = 0b01010100    #84
JEQ = 0b01010101    #85
JNE = 0b01010110    #86

SP = 7              #7


class CPU:
    """Main CPU class."""

    def __init__(self, pc=0, running=True):
        """Construct a new CPU."""
        self.reg = [0] * 8
        self.pc = pc 
        self.ram = [0] * 255
        self.running = running
        self.FL = 0
        self.reg[SP] = 0xF4
          
        self.branch_table = {}
        self.branch_table[LDI] = self.LDI        
        self.branch_table[PRN] = self.PRN
        self.branch_table[HLT] = self.HLT
        self.branch_table[MUL] = self.MUL
        self.branch_table[PUSH] = self.PUSH
        self.branch_table[POP] = self.POP
        self.branch_table[CALL] = self.CALL
        self.branch_table[RET] = self.RET
        self.branch_table[ADD] = self.ADD
        self.branch_table[CMP] = self.CMP
        self.branch_table[JMP] = self.JMP
        self.branch_table[JEQ] = self.JEQ
        self.branch_table[JNE] = self.JNE
        
    """
    The instruction pointed to by the PC is 
    fetched from RAM, decoded, and executed.
    """
    
    
    def ram_read(self, MAR):
        
        return self.ram[MAR] #set the value to Memory Address Register, holds the memory address we're reading or writing
        

    def ram_write(self, MAR, MDR):
        
        self.ram[MAR] = MDR #Memory Data Register, holds the value to write or the value just read
    
    def LDI(self, op, r1, r2):
        
        self.reg[r1] = r2
        
        self.pc += 3
    
    def PRN(self, op, r1, r2):
        
        print(self.reg[r1])
        
        self.pc += 2
    
    def HLT(self, op, r1, r2):
        self.running = False
          
    def MUL(self, op, r1, r2):
        
        self.alu("MUL",r1, r2) 
        
        self.pc += 3
        
    def ADD(self, op, r1, r2):
        self.alu("ADD", r1, r2)
        
        self.pc += 3
        
    def PUSH(self, op, r1, r2):
        #decrement SP pointer
        self.reg[SP] -= 1
        #Copy value in given register
        reg_val = self.reg[r1]
        #Copy value to the address pointed to in stack
        self.ram[self.reg[SP]] = reg_val
        
        self.pc += 2
    
    def POP(self, op, r1, r2):
        #get value at pointer in stack
        reg_val = self.ram[self.reg[SP]]
        #copy value to given register
        self.reg[r1] = reg_val
        # increment Stack Pointer
        self.reg[SP] += 1
        
        self.pc += 2
        
    def CALL(self, op, r1, r2):
        #set return addr
        return_addr = self.pc + 2
        #push it to the stack
        self.reg[SP] -= 1
        self.ram[self.reg[SP]] = return_addr
        # Set ther PC to the subroutine
        self.pc = self.reg[r1]
        
         
        
    
    def RET(self, op, r1, r2):
        #pop the return addr off strack
        self.pc = self.ram[self.reg[SP]]
        
        self.reg[SP] += 1
        
        
        
    def CMP(self, op, r1, r2):
        self.alu("CMP",r1, r2) 
        
        self.pc += 3
    
    def JMP(self, op, r1, r2):
        self.pc = self.reg[r1]
    
        
    def JEQ(self, op, r1, r2):
        if self.FL == 0b00000001:
            self.JMP(op,r1,r2)
        else:
            self.pc += 2
        
    def JNE(self, op, r1, r2):
        if self.FL != 0b00000001:
            self.JMP(op,r1,r2)
        else:
            self.pc += 2
        
    def load(self):
        """Load a program into memory."""

        filename = sys.argv[1]
        address = 0
        with open(filename) as f:
            
            for line in f:
                
                line = line.split("#") 
                
                try:
                     
                    val = int(line[0].strip(), 2)
                    
                    
                except ValueError:
                    continue
                
                self.ram_write(address, val)
                address += 1
    


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        
        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "CMP":
            if self.reg[reg_a] == self.reg[reg_b]:
                self.FL = 0b00000001
            
            
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()
    
    #Main Loop
       
    def run(self):       
        """
        Run the CPU.      
        """    
        while self.running:
            ir = self.ram_read(self.pc)
            op = ir
            op_a = self.ram_read(self.pc + 1)
            op_b = self.ram_read(self.pc + 2)
            # print("IR",ir, "OPA", op_a, "OPB", op_b)
            self.branch_table[ir]( op, op_a, op_b)
            
       
       
m = CPU()
m.load()
# m.run()    