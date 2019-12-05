program = []
with open('input', 'r') as infile:
	inprog = '3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99'
	#inprog = '3,3,1105,-1,9,1101,0,0,12,4,12,99,1'
	#inprog = '3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9'
	#inprog = '3,3,1108,-1,8,3,4,3,99'
	#inprog = '3,9,7,9,10,9,4,9,99,-1,8'
	#inprog = '3,9,8,9,10,9,4,9,99,-1,8'
	inprog = infile.readline().strip()	
	input = inprog.split(',')
	program = list(map(int,input))
	#print ("program length", len(program))

def runprog(input):
	memory = program.copy()
	cur = 0
	while True:
	#for _ in range(10):
		op = memory[cur]
		# parse op to op, modes
		opp = [op%100, op//100]
		inst = []
		if opp[0] == 99:
			return
		elif opp[0] == 3 or opp[0] == 4:
			inst = memory[cur:cur+2]
			cur += 2
			if opp[0] == 3:
				memory[inst[1]] = input
			elif opp[0] == 4:
				a = memory[inst[1]] if opp[1]%10==0 else inst[1]
				print("beep", a)
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



print('#1',runprog(1))
# first try! 13978427

#print('#2-17', runprog(17))

#print('#2-8', runprog(8))

print('#2',runprog(5))
# yaaaay 11189491


