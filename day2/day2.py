program = []
with open('input', 'r') as infile:
	inprog = '1,9,10,3,2,3,11,0,99,30,40,50'
	inprog = '1,0,0,0,99'
	inprog = '2,3,0,3,99'
	inprog = '2,4,4,5,99,0'
	inprog = '1,1,1,4,99,5,6,0,99'
	inprog = infile.readline().strip()	
	input = inprog.split(',')
	program = list(map(int,input))


def runprog(noun,verb):
	memory = program.copy()
	memory[1]=noun
	memory[2]=verb
	cur = 0
	while True:
		inst = memory[cur:cur+4]
		if inst[0] == 99: break
		update = inst[3]
		if inst[0] == 1:
			inst[3] = memory[inst[1]]+memory[inst[2]]
		elif inst[0] == 2:
			inst[3] = memory[inst[1]]*memory[inst[2]]
		else:
			print(f'unexpected {inst[0]} at cur {cur}')
		memory[update]=inst[3]

		cur += 4
	return memory[0]
	#break

print('#1',runprog(12,2))
# too low 1028301 (forgot "1202 program alarm" state)
# 6627023 win!

target = 19690720
for x in range(100):
	for y in range(100):
		if runprog(x,y)==target:
			print('#2',x*100+y)
			break
			# 4019 win!

