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
		#self.phase = phase
		self.base = 0
		self.input = []
		#self.used_phase = False

	def _input(self, val):
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
				#print('end')
				return None 
			elif opp[0] == 3 or opp[0] == 4 or opp[0] == 9:
				inst = [self.memory[n] for n in range(self.cur, self.cur+3)] #self.memory[self.cur:self.cur+2]
				self.cur += 2
				if opp[0] == 3:
					if len(self.input)==0:
						#print('need a move')
						self.cur -=2
						break
						#self._input(0)
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



def printboard(game):
	xm = max([x for (x,y) in game])
	ym = max([y for (x,y) in game])
	board = {0:' ',1:'=',2:'#',3:'-',4:'o'}	
	for y in range(ym+1):
		for x in range(xm+1):
			print(board[game[(x,y)]],end='')
		print()

game = defaultdict(int)

puter = Amp()
for i in range(1000000):
	#puter._input()

	x = puter.runprog()
	if x == None:
		break
	y = puter.runprog()
	if y == None:
		break
	p = puter.runprog()
	if p == None:
		break
	assert p in [0,1,2,3,4]
	game[(x,y)]=p

num_blocks = list(game.values()).count(2)
print('#1',num_blocks)

printboard(game)

puter = Amp()
puter.deposit_coin()
#puter._input(0)
paddle = None
ball = None

sanity = 0
score = 0
while sanity < 10000:
	sanity += 1

	counter = 0
	for i in range(1000000):
		counter+=1
		x = puter.runprog()
		if x == None:
			break
		y = puter.runprog()
		if y == None:
			break
		p = puter.runprog()
		if p == None:
			break
		if x==-1 and y==0:
			#print('score',p, counter)
			counter = 0
			score = p
		else:
			assert p in [0,1,2,3,4]
			#print('...',x,y,p)
			game[(x,y)]=p
			if p == 3:
				paddle = x
			elif p == 4:
				ball = x

	#print('paddle',paddle)
	#print('ball',ball)
	move = 0
	if paddle > ball:
		move = -1
	elif paddle < ball:
		move = 1

	#print('move',move)
	puter._input(move)

print('#2',score)
