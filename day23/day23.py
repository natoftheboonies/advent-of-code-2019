from itertools import permutations
from collections import defaultdict, deque

program = []
with open('input', 'r') as infile:
	inprog = infile.readline().strip()	
	input = inprog.split(',')
	program = list(map(int,input))
	#print(program)
	#print ("program length", len(program))


class Amp:
	def __init__(self, addr, phase=0):
		self.memory = defaultdict(int)
		for k,v in enumerate(program):
			self.memory[k] = v #{k:v for k,v in enumerate(program)}
		self.cur = 0
		self.phase = phase
		self.base = 0
		self.outputs = []
		self.inputs = []
		self.stdout = False
		self.addr = addr
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
		if not self.inputs:
			self.inputs = inputs
		elif inputs != [-1]:
			self.inputs += inputs
		#if not self.addr:
		#	self.addr = inputs[0]


	def runprog(self):
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
					if self.inputs:
						input = self.inputs.pop(0)
					else:
						#print('no input')
						self.cur -=2
						break
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
					self.outputs.append(a)
					if len(self.outputs) == 3:
						message = self.outputs
						self.outputs = []
						#print('outbound message from',self.addr,message)
						return message
					elif len(self.outputs) > 3:
						print('should not get here...')
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


class Network(object):
	"""docstring for Network"""
	def __init__(self):
		super(Network, self).__init__()
		self.computers = []
		self.messages = deque()

	def populate(many):
		for addr in range(many):
			a = Amp(addr)
			a.setinputs([addr])
			self.computers.append()
		

computers = {}
messages = {}


#while sanity < 10000:
for addr in range(50):
	if addr in computers.keys():
		a = computers[addr]
	else:
		a = Amp(addr)
		a.setinputs([addr])
		computers[addr] = a
		messages[addr] = []

sanity = 0

first_nat = None
nat = None
prior_nat = None

while True and sanity < 10000:
	sanity += 1
	network_idle = True
	for addr in range(50):
		a = computers[addr]
		if messages[addr]:
			tellit = messages[addr].pop(0)
			#print('message for',addr, tellit)
			a.setinputs(tellit)
			network_idle = False
		else:
			a.setinputs([-1])
			#print('no message for ',addr)
		
		message = a.runprog()
		while message:
			network_idle = False
			#print('message from',addr,'to',message[0],':',message[1:])
			if message[0]==255:
				nat = message[1:]
				if not first_nat:
					first_nat = nat[:]
					print ('#1',nat[1])
				break
			else:
				messages[message[0]].append(message[1:])
				message = a.runprog()
	
	if network_idle and nat:
		if prior_nat and nat and prior_nat[1]==nat[1]:
			print('#2',nat[1])
			sanity = 100001
			break
		#print('wake up 0',nat, prior_nat)
		messages[0].append(nat)
		prior_nat = nat[:]
		network_idle = False


