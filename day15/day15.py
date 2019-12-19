from collections import defaultdict
import sys

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
		#self.phase = phase
		self.base = 0
		self.input = []
		#self.used_phase = False

	def _input(self, val):
		assert int(val)==val
		self.input.append(val)
		#print('inputs',self.input)
		return self

	def deposit_coin(self):
		self.memory[0]=2
		return None

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

	def runprog(self):
		#slow = 0
		while True:
			#slow+=1
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
					if len(self.input)==0:
						print('need a move')
						self._input(0)
					#if not self.used_phase:
					if opp[1]%10==2:
						self.memory[inst[1]+self.base]=self.input.pop(0)
					else:
						self.memory[inst[1]] = self.input.pop(0)
					#	self.used_phase = True
					#else:
					#	print('shoudl not get here')
					#	self.memory[inst[1]] = input
				elif opp[0] == 4:
					a = self.parm(inst[1],opp[1]%10) #self.memory[inst[1]] if opp[1]%10==0 else inst[1]
					#print("beep", a, self.cur)
					return a # signal
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

game = defaultdict(int)

# move (input): north (1), south (2), west (3), and east (4)
# output: wall (0), moved (1), moved+goal (2)

# first, try all 4 directions

def moveback(i):
	if i == 1:
		return 2
	elif i == 2:
		return 1
	elif i == 3:
		return 4
	elif i == 4:
		return 3

puter = Amp()

path = []
blacklist = defaultdict(list) # {62 : [0]}
blacklist[62] = [0]
blacklist[178] = [0]
blacklist[220] = [0]
blacklist[234] = [0]
blacklist[246] = [0]
blacklist[316] = [0]


for c in range(500):
	currentchoices = []
	choice = 0
	#print(path)
	last = None
	step = 0
	for i in path:
		#print("i",i)
		idx = 0
		if step in blacklist.keys():
			idx = max(blacklist[step])+1

		last = moveback(i[idx])
		puter._input(i[idx])
		y = puter.runprog()
		assert y == 1
		step += 1
	# look where to go next
	valid = []
	for i in range(1,5):
		if i == last:
			continue
		puter._input(i)
		x = puter.runprog()
		if x == 1:
			valid.append(i)
			puter._input(moveback(i))
			y = puter.runprog()
			assert y == 1
		if x == 2:
			valid.append(i)
			print('win!', c)
			sys.exit()
		#print(i,x)
	if len(valid)>1:
		print("valid",valid, "at",c)
	elif len(valid)==0:
		print("stuck", c)
		print(len(path),path)
		sys.exit()

	# return home
	gohome = list(reversed(path))
	#gohome.reverse()
	#print("go home",gohome)
	for i in gohome:
		#print("i",i)
		step -= 1			
		idx = 0
		if step in blacklist.keys():
			idx = max(blacklist[step])+1
		last = moveback(i[idx])
		puter._input(last)
		y = puter.runprog()
		assert y == 1	


	if len(valid)>=1:
		path.append(valid)

#print("path",path)
print("outta gas")

