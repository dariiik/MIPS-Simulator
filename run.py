'''
MIPS-32 Instruction Level Simulatr

CSE261 UNIST
run.py
'''

import util
import initialize
import ctypes


def OPCODE(INST):
    return INST.opcode


def SET_OPCODE(INST, VAL):
    INST.opcode = ctypes.c_short(VAL).value


def FUNC(INST):
    return INST.func_code


def SET_FUNC(INST, VAL):
    INST.func_code = ctypes.c_short(VAL).value


def RS(INST):
    return INST.rs


def SET_RS(INST, VAL):
    INST.rs = ctypes.c_ubyte(VAL).value


def RT(INST):
    return INST.rt


def SET_RT(INST, VAL):
    INST.rt = ctypes.c_ubyte(VAL).value


def RD(INST):
    return INST.rd


def SET_RD(INST, VAL):
    INST.rd = ctypes.c_ubyte(VAL).value


def FS(INST):
    return RD(INST)


def SET_FS(INST, VAL):
    SET_RD(INST, VAL)


def FT(INST):
    return RT(INST)


def SET_FT(INST, VAL):
    SET_RT(INST, VAL)


def FD(INST):
    return SHAMT(INST)


def SET_FD(INST, VAL):
    SET_SHAMT(INST, VAL)


def SHAMT(INST):
    return INST.shamt


def SET_SHAMT(INST, VAL):
    INST.shamt = ctypes.c_ubyte(VAL).value


def IMM(INST):
    return INST.imm


def SET_IMM(INST, VAL):
    INST.imm = ctypes.c_short(VAL).value


def BASE(INST):
    return RS(INST)


def SET_BASE(INST, VAL):
    SET_RS(INST, VAL)


def IOFFSET(INST):
    return IMM(INST)


def SET_IOFFSET(INST, VAL):
    SET_IMM(INST, VAL)


def IDISP(INST):
    X = s(SIGN_EX(INST)) << 2
    return X


def COND(INST):
    return RS(INST)


def SET_COND(INST, VAL):
    SET_RS(INST, VAL)


def CC(INST):
    return (RT(INST) >> 2)


def ND(INST):
    return ((RT(INST) & 0x2) >> 1)


def TF(INST):
    return (RT(INST) & 0x1)


def TARGET(INST):
    return INST.target


def SET_TARGET(INST, VAL):
    INST.target = VAL


def ENCODING(INST):
    return INST.encoding


def SET_ENCODIGN(INST, VAL):
    INST.encoding = VAL


def EXPR(INST):
    return INST.expr


def SET_EXPR(INST, VAL):
    INST.expr = VAL


def SOURCE(INST):
    return INST.source_line


def SET_SOURCE(INST, VAL):
    INST.source_line = VAL


# Sign Extension
def SIGN_EX(X):
    if (X) & 0x8000:
        return X | 0xffff0000
    else:
        return X


COND_UN = 0x1
COND_EQ = 0x2
COND_LT = 0x4
COND_IN = 0x8

# Minimum and maximum values that fit in instruction's imm field
IMM_MIN = 0xffff8000
IMM_MAX = 0x00007fff

UIMM_MIN = 0
UIMM_MAX = (1 << 16)-1


def BRANCH_INST(TEST, TARGET):
    if TEST:
        JUMP_INST(TARGET)


def JUMP_INST(TARGET):
    import util
    util.CURRENT_STATE.PC = TARGET


def LOAD_INST(LD, MASK):
    return (LD & (MASK))


# Procedure: get_inst_info
# Purpose: Read instruction information
def get_inst_info(pc):
    return initialize.INST_INFO[(pc - util.MEM_TEXT_START) >> 2]
def s(x):
    return ctypes.c_int(x).value
def u(x):
    return ctypes.c_uint(x).value
# Procedure: process_instruction
# Purpose: Process one instruction
def process_instruction():
    currentinstruction = get_inst_info(util.CURRENT_STATE.PC)  
    util.CURRENT_STATE.PC += 4 
    opcode = OPCODE(currentinstruction)  
    functioncode = FUNC(currentinstruction)  
    rs = RS(currentinstruction)  
    rt = RT(currentinstruction)  
    rd = RD(currentinstruction)  
    imm = SIGN_EX(IMM(currentinstruction))
    shamt = SHAMT(currentinstruction)  

    # R-type instruction
    if opcode == 0: 
        if functioncode == 0x20: #add
            util.CURRENT_STATE.REGS[rd] = (util.CURRENT_STATE.REGS[rs] + util.CURRENT_STATE.REGS[rt])
        elif functioncode == 0x21: #addu 
            util.CURRENT_STATE.REGS[rd] = u(util.CURRENT_STATE.REGS[rs]) + u(util.CURRENT_STATE.REGS[rt])
        elif functioncode == 0x8: #jr
            JUMP_INST(util.CURRENT_STATE.REGS[currentinstruction.rs]) 
        elif functioncode == 0x2b: #sltu
            util.CURRENT_STATE.REGS[rt] = int(u(util.CURRENT_STATE.REGS[rs]) < u(util.CURRENT_STATE.REGS[rt]))
        elif functioncode == 0x23: #subu
            util.CURRENT_STATE.REGS[rd] =(u(util.CURRENT_STATE.REGS[rs]) - u(util.CURRENT_STATE.REGS[rt]))
        elif functioncode == 0x24: #and
            util.CURRENT_STATE.REGS[rd] = (u(util.CURRENT_STATE.REGS[rs]) & u(util.CURRENT_STATE.REGS[rt]))  
        elif functioncode == 0x27: #nor
            util.CURRENT_STATE.REGS[rd] = ~(u(util.CURRENT_STATE.REGS[rs]) | u(util.CURRENT_STATE.REGS[rt]))  
        elif functioncode == 0x25: #or
            util.CURRENT_STATE.REGS[rd] = (u(util.CURRENT_STATE.REGS[rs]) | u(util.CURRENT_STATE.REGS[rt])) 
        elif functioncode == 0x02: #srl
            util.CURRENT_STATE.REGS[rd] = (u(util.CURRENT_STATE.REGS[rt])>>shamt) 
        elif functioncode == 0x00: #sll
            util.CURRENT_STATE.REGS[rd] = (u(util.CURRENT_STATE.REGS[rt])<<shamt) 
        elif functioncode == 0x2a: #slt
            util.CURRENT_STATE.REGS[rd] = int(util.CURRENT_STATE.REGS[rs] < util.CURRENT_STATE.REGS[rt])
        elif functioncode == 0x22: #sub
            util.CURRENT_STATE.REGS[rd] = (util.CURRENT_STATE.REGS[rs] - util.CURRENT_STATE.REGS[rt])

    else:  # I-type and J-type instructions
        if opcode == 0xf: #lui
            imm = IMM(currentinstruction)
            util.CURRENT_STATE.REGS[rt] = imm << 16 
        elif opcode == 0xd: #ori
            imm = ctypes.c_ushort(IMM(currentinstruction)).value
            util.CURRENT_STATE.REGS[rt] = (util.CURRENT_STATE.REGS[rs] | imm) 
        elif opcode == 0x23: #lw
            util.CURRENT_STATE.REGS[rt] = util.mem_read((util.CURRENT_STATE.REGS[rs]) + s(imm)) 
        elif opcode == 0x2: #jump
            JUMP_INST(TARGET(currentinstruction) << 2)  
        elif opcode == 0x3: #jump and link
            util.CURRENT_STATE.REGS[31] = util.CURRENT_STATE.PC + 4
            JUMP_INST(TARGET(currentinstruction) << 2)   
        elif opcode == 0x5: #bne
            BRANCH_INST((util.CURRENT_STATE.REGS[rs]) != util.CURRENT_STATE.REGS[rt], (util.CURRENT_STATE.PC + (s(imm) << 2))) 
        elif opcode == 0x4: #beq
            BRANCH_INST((util.CURRENT_STATE.REGS[rs]) == util.CURRENT_STATE.REGS[rt], (util.CURRENT_STATE.PC + (s(imm) << 2)))  
        elif opcode == 0x2b: #sw
            util.mem_write((util.CURRENT_STATE.REGS[rs]) + s(imm), util.CURRENT_STATE.REGS[rt])  
        elif opcode == 0xa: #slti
            util.CURRENT_STATE.REGS[rt] = int(util.CURRENT_STATE.REGS[rs] < imm) 
        elif opcode == 0xb: #sltiu
            util.CURRENT_STATE.REGS[rt] = int(u(util.CURRENT_STATE.REGS[rs]) < u(imm))
        elif opcode == 0xc: #andi
            imm = ctypes.c_ushort(IMM(currentinstruction)).value
            util.CURRENT_STATE.REGS[rt] = (util.CURRENT_STATE.REGS[rs] & imm)  
        elif opcode == 0x8: #addi
            util.CURRENT_STATE.REGS[rt] = (util.CURRENT_STATE.REGS[rs] + s(imm))
        elif opcode == 0x9: #addiu
            util.CURRENT_STATE.REGS[rt] = (util.CURRENT_STATE.REGS[rs] + s(imm))

    util.RUN_BIT = (util.CURRENT_STATE.PC - util.MEM_TEXT_START < initialize.text_size)

