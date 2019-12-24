
sample = '''....#
#..#.
#..##
..#..
#....
'''

with open('input','r') as fp:
	sample = fp.read()
	pass

def print_eris(input):
	for t in input:
		print(''.join(t))

def count_bugs(eris,x,y):
	bugs = 0
	for ex, ey in (-1,0),(1,0),(0,-1),(0,1):
		if x+ex < 0 or x+ex >= len(eris[y]):
			continue
		if y+ey < 0 or y+ey >= len(eris):
			continue
		#print('test',x+ex,y+ey)
		if eris[y+ey][x+ex] == '#':
			bugs += 1
			#print('bug',x+ex,y+ey)
	return bugs			

def next_state(eris):
	next_eris = []
	for y in range(len(eris)):
		eris_row = []
		for x in range(len(eris[y])):
			bugs = count_bugs(eris,x,y)
			#print('bugs @',x,y,bugs)
			if eris[y][x]=='.' and (bugs == 1 or bugs == 2):
				# become infested
				eris_row.append('#')
			elif bugs == 1 and eris[y][x]=='#':
				# remains
				eris_row.append('#')
			elif eris[y][x]=='#':
				# dies
				eris_row.append('.')
			else:
				eris_row.append(eris[y][x])
		next_eris.append(eris_row)
	return next_eris

def calc_bio(eris,p=False):
	bio = 0
	count = 0
	for y in range(len(eris)):
		for x in range(len(eris[y])):
			if eris[y][x]=='#':
				bio += 2**count
			if p:
				print(y,x,2**count)
			count+=1
	return bio



input = sample.strip().split('\n')
eris = [list(t) for t in input]
#print('Initial state')
#print_eris(eris)
#print()

bios = []

for t in range(1,500):
	eris = next_state(eris)
	bio = calc_bio(eris)
	if bio in bios:
		print('#1',bio)
		#print_eris(eris)
		#calc_bio(eris,True)
		break
	bios.append(calc_bio(eris))
	#print('After',t,'minutes')
	#print_eris(eris)
	#print()


