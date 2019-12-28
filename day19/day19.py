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
		#self.stdout = True
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

def checkinput(inst):
	comp = Amp()
	comp.setinputs(inst)
	result = comp.runprog(-1)
	return result	


maze = defaultdict(int)
count = 0 
for y in range(50):
	for x in range(50):
		result = checkinput([x,y])
		count += result
		maze[x,y]=result

print('#1',count)
#1 141
#[Finished in 2.8s]

# for y in range(130,131):
# 	for x in range(150,200):
# 		inst = [x,y]
# 		comp = Amp()
# 		comp.setinputs(inst)
# 		result = comp.runprog(-1)
# 		count += result
# 		maze[x,y]=result
# 		print(maze[x,y],end='')
# 	print()		

#beam going \ so check / corners

# for y in range(130,160):
# 	for x in range(150,200):
# 		if maze[x,y]==1 and maze[x-10,y+1] == 1 and maze[x-10,y+10]==1:
# 			candidate = (x-9,y)
# 			passed = True
# 			for sy in range(10):
# 				for sx in range(10):
# 					if maze[candidate[0]+sx,candidate[1]+sy] != 1:
# 						passed = False
# 			if passed:
# 				print("#2",candidate[0]*10000+candidate[1])
# 			#break

#1590137 too low
#1600138 too low
#1650142 too low

# oh, 100x100 not 10x10 :-P

# let's explore down the left side of the beam

# start at 1000,1000
x = y = 1000
found = False
while not found:
	if checkinput([x,y])==1:
		# then we are on bottom-left edge, so check top-right
		if checkinput([x+99,y-99])==1:
			found = True
		else:
			y+=1
	else:
		x+=1 
print(f'found bottom left at x={x}, y={y}')

print('#2',x*10000+(y-99))
#15891369 is wrong
#2 15641348
#[Finished in 3.6s]

