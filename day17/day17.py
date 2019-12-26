from itertools import permutations
from collections import defaultdict

program = []
with open('input', 'r') as infile:
	inprog = infile.readline().strip()	
	input = inprog.split(',')
	program = list(map(int,input))
	#print(program)
	#print ("program length", len(program))


def ascii(a):
	if a == 10:
		return '\n'
	elif a == 35:
		return '#'
	elif a == 46:
		return '.'
	elif a == 94:
		return '^'
	else:
		#print ('unknown ascii',a,chr(a))
		return chr(a)
	return None

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
						print('#2',a)
					else:
						print(ascii(a),end='')
					if a not in self.outputs:
						self.outputs.append(a)
					if not self.stdout:
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

maze = defaultdict(str)

comp = Amp()
y, x = 0,0
y_max, x_max = 0, 0
while True:
	a = comp.runprog(0)
	if a == None:
		break
	if a == 10:
		y += 1
		y_max = max(y,y_max)
		x = 0
	else:
		maze[x,y] = ascii(a)
		x += 1
		x_max = max(x_max,x)

print('x',0,x_max)
print('y',0,y_max)

# find intersections
intersections = []
bot = None
bot_dir = None
for y in range(y_max):
	for x in range(x_max):
		if maze[x,y]=='#': # and x > 1 and x < x_max-1 and y > 1 and y < y_max-1:
			if maze[x-1,y]=='#' and maze[x+1,y]=='#' and maze[x,y-1]=='#' and maze[x,y+1]=='#':
				intersections.append((x,y))
		elif maze[x,y]=='^':
			bot = (x,y)
			bot_dir = 0

#print(intersections)
sum = sum([x*y for (x,y) in intersections])
print('#1',sum)
#1 13580

#print('start',bot)
#comp = Amp()
#comp.setmem(0,2)
#Amp().runprog(2)

# manual walk: R,6,L,12,R,6,R,6,L,12,R,6

#directions: ^0,>1,v2,<3



class Bot:
	def __init__(self, pos, dir=0):
		self.pos = pos
		self.bot_dir = dir
		self.path = []

	def move_bot(self):
		
		bot = self.pos

		north = (bot[0],bot[1]-1)
		east = (bot[0]+1,bot[1])
		south = (bot[0],bot[1]+1)
		west = (bot[0]-1,bot[1])

		if self.bot_dir == 0:
			ahead, left, right = north, west, east
			further = (0,-1)
		elif self.bot_dir == 1:
			ahead, left, right = east, north, south
			further = (1,0)
		elif self.bot_dir == 2:
			ahead, left, right = south, east, west
			further = (0,+1)
		elif self.bot_dir == 3:
			ahead, left, right = west, south, north
			further = (-1,0)
		else:
			print('unexpected bot_dir', bot_dir)

		#print(maze[bot])
		if maze[ahead]=='#':
			#print('go ahead')
			next = (bot[0]+further[0],bot[1]+further[1])
			dist = 0
			while maze[next] == '#':
				bot = next
				next = (bot[0]+further[0],bot[1]+further[1])
				dist += 1
				#print('xxx')
			self.path.append(dist)
			#print(dist,end=',')
			#bot = next
		elif maze[left]=='#':
			self.path.append('L')
			#print('L',end=',')
			self.bot_dir = (self.bot_dir-1)%4
		elif maze[right]=='#':
			self.path.append('R')
			#print('R',end=',')
			self.bot_dir = (self.bot_dir+1)%4
		else:
			return True
		self.pos = bot
		return False


stop = False
sanity = 0
bot = Bot(bot)
while not stop and sanity < 500:
	sanity+=1
	bot.move_bot()

print(','.join([str(x) for x in bot.path]))

# A            A            C                 B              C                 B              C                 B              C                 A
# R,6,L,12,R,6,R,6,L,12,R,6,L,12,R,6,L,8,L,12,R,12,L,10,L,10,L,12,R,6,L,8,L,12,R,12,L,10,L,10,L,12,R,6,L,8,L,12,R,12,L,10,L,10,L,12,R,6,L,8,L,12,R,6,L,12,R,6
# AAA,AAA,CCC,BBB,CCC,BBB,CCC,BBB,CCC,AAA,

# AAA = R,6,L,12,R,6
# BBB = R,12,L,10,L,10
# CCC = L,12,R,6,L,8,L,12

routine = list('A,A,C,B,C,B,C,B,C,A\n')
progA = list('R,6,L,12,R,6\n')
progB = list('R,12,L,10,L,10\n')
progC = list('L,12,R,6,L,8,L,12\n')

video = 'n\n'

inst = [ord(x) for x in routine]
inst += [ord(x) for x in progA]
inst += [ord(x) for x in progB]
inst += [ord(x) for x in progC]
inst += [ord(x) for x in video]
#print(inst)


comp = Amp()
comp.setmem(2)
comp.setinputs(inst)
sanity = 0
while sanity < len(inst):
	a = comp.runprog(inst[0])
	sanity += 1
	if a == None:
		break



