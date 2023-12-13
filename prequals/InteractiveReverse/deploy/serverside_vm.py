
import base64
import time
import sys

FLAG_EQ = 0b0000_0001
FLAG_LESSER = 0b0000_0010
FLAG_BELOW = 0b0000_0100
FLAG_GREATER = 0b0000_1000
FLAG_ABOVE = 0b0001_0000

MOV_IMM	= "1???_????"
MOV_R1_RX  = "0111_1???"
MOV_RX_R1  = "0111_0???"
MOV_MEM_RX = "0110_1???"
MOV_RX_MEM = "0110_0???"

CMP_RX	 = "0101_1???"
ADD_RX	 = "0101_0???"
SUB_RX	 = "0100_1???"
XOR_RX	 = "0100_0???"
AND_RX	 = "0011_1???"
OR_RX	  = "0011_0???"
NOT_RX	 = "0010_1???"
LSL_R1_IMM = "0010_0???"
LSR_R1_IMM = "0001_1???"

JUMP_X	 = "0001_0???"
NOP		= "0000_0000"
SYSCALL	= "0000_0001"
CALL	   = "0000_0010"
RET		= "0000_0011"
SWP		= "0000_0100"

"""
0b0000_xxxx
11 opcodes remain (and one more is unused in JUMP_X)

#########################
# INPUT FILE STRUCTURE

No headers
Code
Data

################
# ACHITECTURE

8 bit registers, 8 bit instructions
8 registers + IP + FLG
16 bit address space: 0 to 0xffff

There is a shadow stack that can hold 16 values

Register R1 is the return register 
Arguments are in R2, R3, R4...
R7:R8 are used to describe (and access) addresses

###########
# OUTPUT

- IP's value
- FLG's value
- A list of each register's value
- The shadow stack
"""

def print_debug():
	print("---- REGISTER INFO ----")
	print("IP:  " + hex(ip))
	print("FLG: " + hex(flg))
	for reg in registers:
		print(reg["name"] + ":  " + hex(reg["value"]))
	print("POINTED ADDRESS: " + hex(get_addr()))
	print("---- CALL  STACK ----")
	print(str(list(map(hex,shadow_stack))))

def crash(msg):
	print("=== PROGRAM CRASHED ===")
	print(msg)
	print_debug()
	exit()


def match_mask(instr, mask):
	shft = mask.count("?")
	bitmask = int(mask.replace("?", "").replace("_", ""), 2)
	return (instr >> shft == bitmask)

def get_register(instr):
	return registers[instr & 7]

def set_register(reg, new_value):
	reg["value"] = new_value & reg["mask"]

def set_memory(value):
	write_addr = get_addr()

	if(write_addr < 0) | (write_addr >= len(memory)):
		crash("Write address out of bounds") # This should never happen

	memory[write_addr] = value & 0xff

def get_addr():
	return (registers[6]["value"] << 8) + registers[7]["value"]


def mov_imm(reg, instr):
	set_register(reg, (instr >> 3) & 0xf)

def mov_r1_rx(reg):
	set_register(registers[0], reg["value"])

def mov_rx_r1(reg):
	set_register(reg, registers[0]["value"])

def mov_mem_rx(reg):
	set_memory(reg["value"])

def mov_rx_mem(reg):
	set_register(reg, memory[get_addr()])

def cmp_rx(reg):
	global flg
	ra = registers[0]["value"]
	rb = reg["value"]
	flg = 0

	if ra < rb:
		flg |= FLAG_BELOW
	if ra == rb:
		flg |= FLAG_EQ
	if ra > rb:
		flg |= FLAG_ABOVE

	if(ra & 0x80):
		ra -= 0x100
	if(rb & 0x80):
		rb -= 0x100

	if ra < rb:
		flg |= FLAG_LESSER
	if ra > rb:
		flg |= FLAG_GREATER

def add_rx(reg):
	set_register(registers[0], registers[0]["value"] + reg["value"])

def sub_rx(reg):
	set_register(registers[0], registers[0]["value"] - reg["value"])

def xor_rx(reg):
	set_register(registers[0], registers[0]["value"] ^ reg["value"])

def and_rx(reg):
	set_register(registers[0], registers[0]["value"] & reg["value"])

def or_rx(reg):
	set_register(registers[0], registers[0]["value"] | reg["value"])

def not_rx(reg):
	set_register(reg, ~reg["value"])

def lsl_r1_imm(instr):
	set_register(registers[0], registers[0]["value"] << (instr & 7))

def lsr_r1_imm(instr):
	set_register(registers[0], registers[0]["value"] >> (instr & 7))

def jump_x(instr):
	global ip
	jump_type = instr & 7

	if(jump_type == 0):
		crash("Unknown instruction")
	elif(jump_type == 1):
		ip = get_addr()
	elif(jump_type == 2) & (flg & FLAG_EQ):
		ip = get_addr()
	elif(jump_type == 3) and not (flg & FLAG_EQ):
		ip = get_addr()
	elif(jump_type == 4) & (flg & FLAG_LESSER):
		ip = get_addr()
	elif(jump_type == 5) & (flg & FLAG_BELOW):
		ip = get_addr()
	elif(jump_type == 6) & (flg & FLAG_GREATER):
		ip = get_addr()
	elif(jump_type == 7) & (flg & FLAG_ABOVE):
		ip = get_addr()

def syscall():
	syscall_type = registers[0]["value"]

	if(syscall_type == 0):
		exit()
	elif(syscall_type == 1):	# reads one byte of input to r1
		try:
			value = sys.stdin.read(1)
			set_register(registers[0], ord(value))
		except:
			crash("Read syscall failed")
	elif(syscall_type == 2):	# writes one byte of input to stdout
		#sys.stdout.buffer.write(bytes([memory[get_addr()]]))
		sys.stdout.buffer.write(bytes([registers[1]["value"]]))
		sys.stdout.flush()
	elif(syscall_type == 3):	# unlocks room
		sys.stdout.write("o-~-~-~-~-~-~-~-~-~-o\n|   LOCK RELEASED   |\n\\-------------------/")
		sys.stdout.flush()
	else:
		crash("Unknown syscall")

def call():
	global ip
	if(len(shadow_stack) < 16):
		shadow_stack.append(ip)
		ip = get_addr()
	else:
		crash("Attempted a call although shadow stack is full")

def ret():
	global ip
	if(len(shadow_stack) > 0):
		ip = shadow_stack.pop()
	else:
		crash("Attempted a return although shadow stack is empty")

def swp():
	tmp = registers[7]["value"]
	registers[7]["value"] = registers[5]["value"]
	registers[5]["value"] = tmp

	tmp = registers[6]["value"]
	registers[6]["value"] = registers[4]["value"]
	registers[4]["value"] = tmp


def load_program_into_memory():
	print("Welcome to my VM. Before I run, you will have to load some firmware. To do this, follow these steps:")
	print("  - Send the following string ended by a newline: '-----PROGRAM START-----'")
	print("  - Send your program (like the content of prog.bin) encoded in base64, then ended by a newline")
	print("  - Send the following string ended by a newline: '-----PROGRAM END-----'")
	print("If you follow these steps, we shall confirm VM execution has started and then run your program.")
	
	if input() != "-----PROGRAM START-----":
		print("Did not find program start banner")
		exit()
	
	base_64_encoded = input()

	try:
		program = base64.b64decode(base_64_encoded)
	except:
		print("Unable to decode base 64")
		exit()

	program = program[:0x10000]
	for i in range(len(program)):
		memory[i] = program[i]

	if input() != "-----PROGRAM END-----":
		print("Did not find program end banner")
		exit()

	print("+-----------------------------+")
	print("| THE FIRMWARE IS RUNNING NOW |")
	print("+-----------------------------+")
	time.sleep(0.5)


registers = [{
		"name":"R" + str(i + 1),
		"value":0,
		"mask":0xff
	} for i in range(8)]

flg = 0
ip = 0x0
memory = [0] * 0xffff
shadow_stack = []

def main():
	global ip

	load_program_into_memory()

	while True:
		if ip >= len(memory):
			crash("Instruction pointer went out of memory range")

		instr = memory[ip]
		reg = get_register(instr)
		if match_mask(instr, MOV_IMM):
			mov_imm(reg, instr)
		elif match_mask(instr, MOV_R1_RX):
			mov_r1_rx(reg)
		elif match_mask(instr, MOV_RX_R1):
			mov_rx_r1(reg)
		elif match_mask(instr, MOV_MEM_RX):
			mov_mem_rx(reg)
		elif match_mask(instr, MOV_RX_MEM):	  
			mov_rx_mem(reg)
		elif match_mask(instr, CMP_RX):
			cmp_rx(reg)
		elif match_mask(instr, ADD_RX):  
			add_rx(reg)
		elif match_mask(instr, SUB_RX):  
			sub_rx(reg)
		elif match_mask(instr, XOR_RX):  
			xor_rx(reg)
		elif match_mask(instr, AND_RX):  
			and_rx(reg)
		elif match_mask(instr, OR_RX):  
			or_rx(reg)
		elif match_mask(instr, NOT_RX):   
			not_rx(reg)
		elif match_mask(instr, LSL_R1_IMM):  
			lsl_r1_imm(instr)
		elif match_mask(instr, LSR_R1_IMM):  
			lsr_r1_imm(instr)
		elif match_mask(instr, JUMP_X):  
			jump_x(instr)
			#print("\033[31mIP:  " + hex(ip) + "\033[0m")
			#print("FLG: " + hex(flg))
			#print(",  ".join([reg["name"] + ": " + hex(reg["value"]) for reg in registers]))
		elif match_mask(instr, SYSCALL):  
			syscall()
		elif match_mask(instr, CALL): 
			call()
		elif match_mask(instr, RET):	
			ret()
		elif match_mask(instr, SWP):
			swp()
		elif match_mask(instr, NOP):	
			pass
		else:
			crash("Unknown instruction")

		#print("\033[31mIP:  " + hex(ip) + "\033[0m")
		#print("FLG: " + hex(flg))
		#print(",  ".join([reg["name"] + ": " + hex(reg["value"]) for reg in registers]))

		ip = (ip + 1) & 0xffff

if __name__ == "__main__":
	try:
		main()
	except:
		crash("Unknown error")
