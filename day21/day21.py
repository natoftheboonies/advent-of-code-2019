from itertools import permutations
from collections import defaultdict

program = []
with open('input', 'r') as infile:
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
		self.phase = phase
		self.base = 0
		self.outputs = []
		self.inputs = []
		self.stdout = False
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

	def setmem(self,val,loc=0):
		self.memory[loc]=val
		self.stdout = True
		return None

	def setinputs(self,inputs):
		#input.reverse()
		self.inputs = inputs

	def runprog(self, input):
		while True:
			op = self.memory[self.cur]
			# parse op to op, modes
			opp = [op%100, op//100]
			inst = []
			if opp[0] == 99:
				print('exit')
				#print(self.outputs)
				return None 
			elif opp[0] == 3 or opp[0] == 4 or opp[0] == 9:
				inst = [self.memory[n] for n in range(self.cur, self.cur+3)] #self.memory[self.cur:self.cur+2]
				self.cur += 2
				if opp[0] == 3:
					input = self.inputs.pop(0)
					#print('input?', input, chr(input))
					#if not self.used_phase:
					if opp[1]%10==2:
						self.memory[inst[1]+self.base]=input
					else:
						#print('phase')
						self.memory[inst[1]] = input #self.phase
					#	self.used_phase = True
					#else:
					#	print('shoudl not get here')
					#	self.memory[inst[1]] = input
				elif opp[0] == 4:
					a = self.parm(inst[1],opp[1]%10) #self.memory[inst[1]] if opp[1]%10==0 else inst[1]
					#print("beep", a, self.cur)
					if a > 10000:
						#print('#1',a)
						return a
					else:
						print(chr(a),end='')
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


# the sample instructions with OR instead of AND ...
inst = '''NOT A J
NOT B T
OR T J
NOT C T
OR T J
AND D J
WALK
'''

#print([ord(x) for x in inst])

comp = Amp()
comp.setinputs([ord(x) for x in inst])
while True:
	a = comp.runprog(0)
	if a == None:
		break
	elif a > 10000:
		print ("#1",a)	


# _ABCDEFGHI
# 0123456789
# jump goes 3, so from _ to D.  
# But, can't land on a D when H is a hole.
# So don't jump if C is a hole unless H is solid.
'''
jump when:
- not A and D
- not B and D
- not C and H and D
(!A or !B or (!C and H)) and D

not C and H first, cuz OR'd with other jump conditions
AND D last cuz AND'd with rest
'''

inst = '''NOT C J
AND H J
NOT A T
OR T J
NOT B T
OR T J
AND D J
RUN
'''

comp = Amp()
comp.setinputs([ord(x) for x in inst])
while True:
	a = comp.runprog(0)
	if a == None:
		break
	elif a > 10000:
		print ("#2",a)	

