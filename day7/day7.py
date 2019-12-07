from itertools import permutations

program = []
with open('input', 'r') as infile:
	inprog = '3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0' # goal: 43210
	inprog = '3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0' # goal 54321
	inprog = '3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0' # goal 65210
	# part 2
	inprog = '3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5' # 139629729
	inprog = '3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10' # 18216
	inprog = infile.readline().strip()	
	input = inprog.split(',')
	program = list(map(int,input))
	#print ("program length", len(program))


def runprog(memory, input, cur=0):
	#memory = program.copy()
	incur = 0
	#cur = 0
	while True:
	#for _ in range(10):
		op = memory[cur]
		# parse op to op, modes
		opp = [op%100, op//100]
		inst = []
		if opp[0] == 99:
			return (-1,cur) # signal, cursor
		elif opp[0] == 3 or opp[0] == 4:
			inst = memory[cur:cur+2]
			cur += 2
			if opp[0] == 3:
				memory[inst[1]] = input[incur]
				incur+=1
			elif opp[0] == 4:
				a = memory[inst[1]] if opp[1]%10==0 else inst[1]
				#print("beep", a, cur)
				return (a, cur) # signal, cursor
		elif opp[0] == 5 or opp[0] == 6:
			inst = memory[cur:cur+3]
			cur += 3
			a = memory[inst[1]] if opp[1]%10==0 else inst[1]
			b = memory[inst[2]] if opp[1]//10==0 else inst[2]
			#print('jump inst', inst,'opp', opp, 'a, b', a, b)
			if (opp[0] == 5 and a != 0) or (opp[0] == 6 and a == 0):
				cur = b
				#print('jump to',cur)
		else:
			inst = memory[cur:cur+4]
			cur += 4			
			a = memory[inst[1]] if opp[1]%10==0 else inst[1]
			b = memory[inst[2]] if opp[1]//10==0 else inst[2]			
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
				print(f'unexpected {inst[0]} at cur {cur}')
			memory[update]=inst[3]

class Amp:
	def __init__(self,phase):
		self.memory = program.copy()
		self.cur = 0
		self.phase = phase

	def runprog(self, input):
		
		#cur = 0
		while True:
		#for _ in range(10):
			op = self.memory[self.cur]
			# parse op to op, modes
			opp = [op%100, op//100]
			inst = []
			if opp[0] == 99:
				return -1 # signal, cursor
			elif opp[0] == 3 or opp[0] == 4:
				inst = self.memory[self.cur:self.cur+2]
				self.cur += 2
				if opp[0] == 3:
					if self.phase:
						self.memory[inst[1]] = self.phase
						self.phase = None
					else:
						self.memory[inst[1]] = input
				elif opp[0] == 4:
					a = self.memory[inst[1]] if opp[1]%10==0 else inst[1]
					#print("beep", a, self.cur)
					return a # signal
			elif opp[0] == 5 or opp[0] == 6:
				inst = self.memory[self.cur:self.cur+3]
				self.cur += 3
				a = self.memory[inst[1]] if opp[1]%10==0 else inst[1]
				b = self.memory[inst[2]] if opp[1]//10==0 else inst[2]
				#print('jump inst', inst,'opp', opp, 'a, b', a, b)
				if (opp[0] == 5 and a != 0) or (opp[0] == 6 and a == 0):
					self.cur = b
					#print('jump to',self.cur)
			else:
				inst = self.memory[self.cur:self.cur+4]
				self.cur += 4			
				a = self.memory[inst[1]] if opp[1]%10==0 else inst[1]
				b = self.memory[inst[2]] if opp[1]//10==0 else inst[2]			
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
				self.memory[update]=inst[3]	


# input is [phase, signal]
max = 0
maxt = None
for t in permutations([0,1,2,3,4]):
	signal = 0
	for phase in t:
		signal = runprog(program.copy(),[phase, signal],0)[0]
	if signal > max:
		max = signal
		maxt = t
		#print('#1',signal,'from',t)
		
print('#1',max,'from',maxt)


maxoutsignal = 0
best_t = None

for t in permutations([5,6,7,8,9]):
	end = False
	signal = [0]*5
	outsignal = signal[0]
	amps = [Amp(phase) for phase in t]
	#cur = [0]*5
	sanity = 0
	while not end and sanity < 100:
		sanity+=1
		outsignal = signal[0]
		for prog in range(5):
			p_next = (prog+1)%5
			#print('runprog:',prog,signal[prog])
			
			signal[p_next] = amps[prog].runprog(signal[prog])
			#print('cursors',cur)
			#print('signals',signal)
			if signal[p_next] == -1:
				end = True
	if outsignal > maxoutsignal:
		maxoutsignal = outsignal
		best_t = t

#print('sanity',sanity)
print('#2', maxoutsignal,'from', best_t)







