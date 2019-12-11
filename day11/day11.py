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

def doturn(dir, turn):
	if turn==0: # left
		if dir == 'L': 
			dir = 'D'
		elif dir == 'D': 
			dir = 'R'
		elif dir == 'R':
			dir = 'U'
		elif dir == 'U':
			dir = 'L'
		else:
			print('unexpected dir',dir)
	elif turn==1: # right
		if dir == 'L': 
			dir = 'U'
		elif dir == 'U': 
			dir = 'R'
		elif dir == 'R':
			dir = 'D'
		elif dir == 'D':
			dir = 'L'
		else:
			print('unexpected dir',dir)
	else:
		print('unexpected turn',turn)
	return dir

def move(d, loc):
	x = 0
	y = 0		
	if d == 'L':
		x = -1
	elif d == 'R':
		x = 1
	elif d == 'U':
		y = 1
	elif d == 'D':
		y = -1
	else:
		print("unexpected direction", d)
	loc=loc[0]+x,loc[1]+y
	return loc

d = 'U' # start up
loc = (0,0)
ship = defaultdict(int)

puter = Amp()
while True:
	puter._input(ship[loc])
	paint = puter.runprog()
	if paint==None:
		break
	ship[loc] = paint
	turn = puter.runprog()
	if turn == None:
		break
	d = doturn(d, turn)
	loc = move(d, loc)

print('#1', len(ship.keys()))
# 13 too low, 50 too low
# 2041

d = 'U' # start up
loc = (0,0)
ship = defaultdict(int)
ship[loc] = 1

puter = Amp()
for x in range(1000000):
	puter._input(ship[loc])
	paint = puter.runprog()
	if paint==None:
		break
	ship[loc] = paint
	turn = puter.runprog()
	if turn == None:
		break
	d = doturn(d, turn)
	loc = move(d, loc)

points = ship.keys()
xl = min(t[0] for t in points)
xh = max(t[0] for t in points)
yl = min(t[1] for t in points)
yh = max(t[1] for t in points)

#print(len(ship.keys()))
#print(xl,xh,yl,yh)
#0 42 -5 0 oh we don't need to make a grid

print('#2') # aak, upside down!
for y in range(yh,yl-1,-1):
	for x in range(xl,xh+1):
		printme = ' '
		if ship[(x,y)]==1:
			printme = 'X'
		print(printme,end='')
	print('')
# ZRZPKEZR

