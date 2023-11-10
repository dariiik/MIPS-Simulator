'''
MIPS-32 Instruction Level Simulatr

CSE261 UNIST
parse.py
'''

import util
import initialize
import ctypes
    
def SET_IMM(INST, VAL):
    INST.imm = ctypes.c_short(VAL).value

def parse_instr(buffer, index):
    instr = util.instruction()
    instr.value = util.fromBinary(buffer)
    instr.opcode = util.fromBinary(buffer[0:6])
    if instr.opcode == 0x0:
        instr.rs = util.fromBinary(buffer[6:11])
        instr.rt = util.fromBinary(buffer[11:16])
        instr.rd = util.fromBinary(buffer[16:21])
        instr.shamt = util.fromBinary(buffer[21:26])
        instr.func_code = util.fromBinary(buffer[26:])
        instr.value = util.fromBinary(buffer)
    elif instr.opcode == 0x2 or instr.opcode == 0x3:
        instr.target = util.fromBinary(buffer[6:])
        instr.value = util.fromBinary(buffer)
    else:
        instr.rs = util.fromBinary(buffer[6:11])
        instr.rt = util.fromBinary(buffer[11:16])
        SET_IMM(instr, util.fromBinary(buffer[16:]))
        #instr.imm = util.fromBinary(buffer[16:])
        #if instr.imm >= (1<<15): #is imm negative
        #    instr.imm -= (1<<16)
        #    instr.value = util.fromBinary(buffer)
    util.mem_write(util.MEM_TEXT_START + index, util.fromBinary(buffer))
    return instr

def parse_data(buffer, index):
    # Implement this function
    # erase "pass" to start implementing
    dataval = util.fromBinary(buffer)
    addressofmem = util.MEM_DATA_START + index
    util.mem_write(addressofmem, dataval)
    


def print_parse_result(INST_INFO):
    print("Instruction Information")

    for i in range(initialize.text_size//4):
        print("INST_INFO[", i, "].value : ", "%8x" % INST_INFO[i].value)
        print("INST_INFO[", i, "].opcode : ", INST_INFO[i].opcode)

        # TYPE I
        # 0xa: (0b001010)SLTI
        # 0x8: (0b001000)ADDI
        # 0x9: (0b001001)ADDIU
        # 0xc: (0b001100)ANDI
        # 0xf: (0b001111)LUI
        # 0xd: (0b001101)ORI
        # 0xb: (0b001011)SLTIU
        # 0x23: (0b100011)LW
        # 0x2b: (0b101011)SW
        # 0x4: (0b000100)BEQ
        # 0x5: (0b000101)BNE
        if INST_INFO[i].opcode == 0xa or \
            INST_INFO[i].opcode == 0x8 or \
            INST_INFO[i].opcode == 0x9 or \
            INST_INFO[i].opcode == 0xc or \
            INST_INFO[i].opcode == 0xf or \
            INST_INFO[i].opcode == 0xd or \
            INST_INFO[i].opcode == 0xb or \
            INST_INFO[i].opcode == 0x23 or \
            INST_INFO[i].opcode == 0x2b or \
            INST_INFO[i].opcode == 0x4 or \
            INST_INFO[i].opcode == 0x5:
            print("INST_INFO[", i, "].rs : ", INST_INFO[i].rs)
            print("INST_INFO[", i, "].rt : ", INST_INFO[i].rt)
            print("INST_INFO[", i, "].imm : ",
                  INST_INFO[i].imm)
            
        # TYPE R
        # 0x0: (0b000000)ADD, SLT, ADDU, AND, NOR, OR, SLTU, SLL, SRL, SUBU  if JR
        elif INST_INFO[i].opcode == 0x0:
            print("INST_INFO[", i, "].func_code : ",
                  INST_INFO[i].func_code)
            print("INST_INFO[", i, "].rs : ",
                  INST_INFO[i].rs)
            print("INST_INFO[", i, "].rt : ",
                  INST_INFO[i].rt)
            print("INST_INFO[", i, "].rd : ",
                  INST_INFO[i].rd)
            print("INST_INFO[", i, "].shamt : ",
                  INST_INFO[i].shamt)

        # TYPE J
        # 0x2: (0b000010)J
        # 0x3: (0b000011)JAL
        elif INST_INFO[i].opcode == 0x2 or INST_INFO[i].opcode == 0x3:
            print("INST_INFO[", i, "].target : ",
                  INST_INFO[i].target)
        else:
            print("Not available instrution\n")

    print("Memory Dump - Text Segment\n")
    for i in range(0, initialize.text_size, 4):
        print("text_seg[", i, "] : ", "%x" %
              util.mem_read(util.MEM_TEXT_START + i))
    for i in range(0, initialize.data_size, 4):
        print("data_seg[", i, "] : ", "%x" %
              util.mem_read(util.MEM_DATA_START + i))
    print("Current PC: %x" % util.CURRENT_STATE.PC)