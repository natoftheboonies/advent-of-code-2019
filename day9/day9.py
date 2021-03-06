from itertools import permutations
from collections import defaultdict

program = []
with open('input', 'r') as infile:
	inprog = '1102,34915192,34915192,7,4,7,99,0' 
	inprog = '104,1125899906842624,99'
	inprog = '109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99'
	inprog = infile.readline().strip()	
	input = inprog.split(',')
	program = list(map(int,input))
	#print(program)
	#print ("program length", len(program))

class Amp:
	def __init__(self, phase=0):
		self.memory = defaultdict(int)
		for k,v in enumerate(program):
			self.memory[k] = v #{k:v for k,v in enumerate(program)}
		self.cur = 0
		#self.phase = phase
		self.base = 0
		#self.used_phase = False

	def parm(self, val, mode):

		if mode==0:
			return self.memory[val]
		elif mode==1:
			return val
		elif mode==2:
			return self.memory[val+self.base]
		else:
			print ('unexpected mode', mode)
			return None

	def runprog(self, input):
		while True:
			op = self.memory[self.cur]
			# parse op to op, modes
			opp = [op%100, op//100]
			inst = []
			if opp[0] == 99:
				print('end')
				return None 
			elif opp[0] == 3 or opp[0] == 4 or opp[0] == 9:
				inst = [self.memory[n] for n in range(self.cur, self.cur+3)] #self.memory[self.cur:self.cur+2]
				self.cur += 2
				if opp[0] == 3:
					#if not self.used_phase:
					if opp[1]%10==2:
						self.memory[inst[1]+self.base]=input
					else:
						self.memory[inst[1]] = self.phase
					#	self.used_phase = True
					#else:
					#	print('shoudl not get here')
					#	self.memory[inst[1]] = input
				elif opp[0] == 4:
					a = self.parm(inst[1],opp[1]%10) #self.memory[inst[1]] if opp[1]%10==0 else inst[1]
					print("beep", a, self.cur)
					#return a # signal
				elif opp[0] == 9:
					a = self.parm(inst[1],opp[1]%10) #self.memory[inst[1]] if opp[1]%10==0 else inst[1]
					self.base += a
					#print('base',self.base)

			elif opp[0] == 5 or opp[0] == 6:
				inst = [self.memory[n] for n in range(self.cur, self.cur+4)] # self.memory[self.cur:self.cur+3]
				self.cur += 3
				a = self.parm(inst[1],opp[1]%10) #self.memory[inst[1]] if opp[1]%10==0 else inst[1]
				b = self.parm(inst[2],opp[1]//10%10) #self.memory[inst[2]] if opp[1]//10==0 else inst[2]
				#print('jump inst', inst,'opp', opp, 'a, b', a, b)
				if (opp[0] == 5 and a != 0) or (opp[0] == 6 and a == 0):
					self.cur = b
					#print('jump to',self.cur)
			else:
				inst = [self.memory[n] for n in range(self.cur, self.cur+5)] # self.memory[self.cur:self.cur+4]
				self.cur += 4			
				a = self.parm(inst[1],opp[1]%10) #self.memory[inst[1]] if opp[1]%10==0 else inst[1]
				b = self.parm(inst[2],opp[1]//10%10) #self.memory[inst[2]] if opp[1]//10==0 else inst[2]			
				#print('inst', inst,'opp', opp, 'a, b', a, b)
				update = inst[3]
				if opp[0] == 1:
					inst[3] = a+b
				elif opp[0] == 2:
					inst[3] = a*b
				elif opp[0] == 7:
					if a < b:
						inst[3] = 1
					else:
						inst[3] = 0
				elif opp[0] == 8:
					if a == b:
						inst[3] = 1
					else:
						inst[3] = 0 
				else:
					print(f'unexpected {inst[0]} at cur {self.cur}')
				if opp[1]//100%10 == 2:
					self.memory[update+self.base] = inst[3]
				else:
					self.memory[update]=inst[3]	

print('#1')
Amp().runprog(1)
# 203 too low
# 160390799 too low

print('#2')
Amp().runprog(2)
