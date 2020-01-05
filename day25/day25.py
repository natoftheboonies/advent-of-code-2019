from itertools import permutations, combinations
from collections import defaultdict, deque

program = []
with open('input', 'r') as infile:
	inprog = infile.readline().strip()	
	input2 = inprog.split(',')
	program = list(map(int,input2))
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
					print(chr(a),end='')
					self.outputs.append(a)
					if False and len(self.outputs) == 3:
						message = self.outputs
						self.outputs = []
						#print('outbound message from',self.addr,message)
						return message
					elif False and len(self.outputs) > 3:
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
					#print('comp',a,b)
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
		return True


# checkpoint at -3,1

a = Amp()

# collect all the stuff that doesn't explode
mypath = '''north
north
take sand
south
south
south
take space heater
south
east
take loom
west
north
north
west
south
take planetoid
north
west
take festive hat
east
east
south
west
take wreath
south
take space law space brochure
south
take pointer
north
north
east
north
inv
west
west
south
west
inv'''.split('\n')

items = '''planetoid
festive hat
space heater
loom
space law space brochure
sand
pointer
wreath'''.split('\n')

blah = a.runprog()

while len(mypath)>0:
	command = mypath.pop(0)
	print(command)
	a.setinputs(list(map(ord,command+'\n')))
	blah = a.runprog()	

for item in items:
	command = 'drop '+item
	print(command)
	a.setinputs(list(map(ord,command+'\n')))
	blah = a.runprog()


found = False
for r in range(4,5):
	if found == True:
		break
	for comb in combinations(items,r):
		if found == True:
			break
		print(comb)
		takes = ['take '+x for x in comb]
		drops = ['drop '+x for x in comb]
		for command in takes+['north']+drops:
			a.setinputs(list(map(ord,command+'\n')))
			blah = a.runprog()
			if blah == None:
				found = True
				break

#('planetoid', 'sand', 'pointer', 'wreath')

# Santa notices your small droid, looks puzzled for a moment, realizes what has happened, and radios your ship directly.
#"Oh, hello! You should be able to get in by typing 529920 on the keypad at the main airlock."

while False:
	command = input()
	a.setinputs(list(map(ord,command+'\n')))
	blah = a.runprog()
	if blah == None:
		break


