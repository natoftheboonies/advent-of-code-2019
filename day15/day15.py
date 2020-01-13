from collections import defaultdict, deque
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

NORTH, SOUTH, EAST, WEST = 1,2,3,4

def turnright(i):
	if i == NORTH:
		return EAST
	elif i == SOUTH:
		return WEST
	elif i == EAST:
		return SOUTH
	elif i == WEST:
		return NORTH	

def turnleft(i):
	if i == NORTH:
		return WEST
	elif i == SOUTH:
		return EAST
	elif i == EAST:
		return NORTH
	elif i == WEST:
		return SOUTH	

def moveback(i):
	if i == 1:
		return 2
	elif i == 2:
		return 1
	elif i == 3:
		return 4
	elif i == 4:
		return 3


def trytomove(puter, move):
	puter._input(move)
	x = puter.runprog()
	return x

def movecoords(movedir):
	if movedir == NORTH:
		return (0,-1)
	elif movedir == SOUTH:
		return (0,1)
	elif movedir == EAST:
		return (1,0)
	elif movedir == WEST:
		return (-1,0)
	else:
		print('unexpected move',movedir)

puter = Amp()

botdir = NORTH
botpos = (0,0)

#game[botpos] = 1 # starting position is not wall or goal
game = set()
game.add(botpos)
goal = None

for _ in range(10000):
	botdir = turnright(botdir)
	movepos = movecoords(botdir)
	newpos = (botpos[0]+movepos[0],botpos[1]+movepos[1])
	well = trytomove(puter,botdir)
	if well == 0: # wall right
		#game[newpos] = well
		# right blocked, try straight
		botdir = turnleft(botdir)
		movepos = movecoords(botdir)
		newpos = (botpos[0]+movepos[0],botpos[1]+movepos[1])
		well = trytomove(puter,botdir)
		if well == 0: # wall straight
			#game[newpos] = well	
			# straight blocked, try left
			botdir = turnleft(botdir)
			movepos = movecoords(botdir)
			newpos = (botpos[0]+movepos[0],botpos[1]+movepos[1])
			well = trytomove(puter,botdir)
			if well == 0: # wall left
				pass
				#print('we stuck')
				#game[newpos] = well
				# but now botdir is left, so we can just loop				
			else: # left not a wall
				botpos = newpos
				game.add(botpos)
				if well == 2:
					#print('found air!')
					goal = botpos

		else: # straight not a wall
			botpos = newpos
			game.add(botpos)
			if well == 2:
				#print('found air!')
				goal = botpos
	else: # right not a wall
		botpos = newpos
		game.add(botpos)
		if well == 2:
			#print('found air!', botpos)
			goal = botpos

	if botpos==(0,0) and botdir == 1:
		#print('we home', t)
		break

#print('air at', goal)


def find_neighbors(game, node): # node is (x,y)
	valid = []
	for move in (0,1),(0,-1),(1,0),(-1,0):
		check = (node[0]+move[0],node[1]+move[1])
		if check in game:
			valid.append(check)
	return valid


#ok, now we can BFS through game to find goal.

def bfs_search(game, start, goal):
	explored = set() # set needs flattened tuple
	queue = deque([[start]]) #[[start]]
	maxlen = 0
	while queue:
		path = queue.popleft()
		#print(path)
		node = path[-1]
		if node not in explored:
			neighbors = find_neighbors(game, node)
			for neighbor in neighbors:
				if neighbor in explored:
					continue
				new_path = list(path)
				new_path.append(neighbor)
				queue.append(new_path)
				if len(new_path)>maxlen:
					maxlen = len(new_path)
				#print(new_path)
				if neighbor == goal:
					#print('goal!', new_path)
					return new_path

			explored.add(node)
	return maxlen


shortest_path = bfs_search(game,(0,0),goal)
print("#1",len(shortest_path)-1)

# hmm, to spread oxygen start at goal and find longest path
longest_path = bfs_search(game,goal,None)
print("#2",longest_path-1)


#print("path",path)
#print("outta gas")

