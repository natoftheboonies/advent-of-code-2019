


def print_eris(input,title=None):
	if title:
		print(title)
	for t in input:
		print(''.join(t))
	print ()

def part1(eris):

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
		for y in range(len(eris)):
			for x in range(len(eris[y])):
				if eris[y][x]=='#':
					bio += 2**(5*y+x)
				if p:
					print(y,x,2**(5*y+x))
		return bio



	bios = []

	for t in range(1,500):
		eris = next_state(eris)
		bio = calc_bio(eris)
		if bio in bios:
			return bio
			#print('#1',bio)
			#print_eris(eris)
			#calc_bio(eris,True)
			break
		bios.append(calc_bio(eris))
		#print('After',t,'minutes')
		#print_eris(eris)
		#print()


sample = '''....#
#..#.
#..##
..#..
#....
'''

with open('input','r') as fp:
	sample = fp.read()
	pass

input = sample.strip().split('\n')
eris = [list(t) for t in input]
#print('Initial state')
print_eris(eris)
#print()
print('#1',part1(eris))


### recursive grids, (2,2) is next level:
# base = 0, inner = +1, outer = -1
# inner (+1) grows if:
# * (2,1) & (1,2), top-left corner (0,0)
# * (2,1) & (3,2), top-right corner (4,0)
# * (2,3) & (1,2), bottom-left corner (0,4)
# * (2,3) & (3,2), bottom-right corner (4,4)
# outer (-1) grows if:
# * exactly 2 on an edge (2,1),(1,2),(3,2),(2,3)


# 01234
# 1....
# 2.?..
# 3....
# 4....

def part2(eris):

	def new_inner_eris(eris):
		#print('given outer')
		#print_eris(eris)
		eris_in = [['.']*5 for _ in range(5)]
		eris_in[2][2] = '?'
		if eris[2][1] == '#':
			for y in range(5):
				eris_in[y][0] = '#'
		if eris[2][3] == '#':
			for y in range(5):
				eris_in[y][4] = '#'
		if eris[1][2] == '#':
			for x in range(5):
				eris_in[0][x] = '#'
		if eris[3][2] == '#':
			for x in range(5):
				eris_in[4][x] = '#'
		#print('grew inner')
		#print_eris(eris_in)
		return eris_in		

	def new_outer_eris(eris):
		#print('given inner')
		#print_eris(eris)
		eris_out = [['.']*5 for _ in range(5)]
		eris_out[2][2] = '?'
		eris_out[1][2] = '#' if eris[0].count('#') in (1,2) else '.' # top
		eris_out[2][1] = '#' if [x[0] for x in eris].count('#') in (1,2) else '.' # left
		eris_out[2][3] = '#' if [x[4] for x in eris].count('#') in (1,2) else '.' # right
		eris_out[3][2] = '#' if eris[4].count('#') in (1,2) else '.' # bottom
		#print('grew outer')
		#print_eris(eris_out)
		return eris_out

	def count_bugs(eris,x,y,outer,inner):
		bugs = 0
		for ex, ey in (-1,0),(1,0),(0,-1),(0,1):
			
			if 0 <= x+ex < len(eris[y]) and 0 <= y+ey < len(eris):
				if eris[y+ey][x+ex] == '#':
					bugs += 1

			if x+ex < 0:
				if outer and outer[2][1]=='#':
					bugs += 1
			elif x+ex >= len(eris[y]):
				if outer and outer[2][3]=='#':
					bugs += 1
			if y+ey < 0:
				if outer and outer[1][2]=='#':
					bugs += 1
			elif y+ey >= len(eris):
				if outer and outer[3][2]=='#':
					bugs += 1
			if y+ey==x+ex==2:
				#inner!
				if not inner:
					continue
				if ey == -1: # bottom
					bugs += inner[4].count('#')
				elif ey == 1: # top
					bugs += inner[0].count('#')
				elif ex == -1: # right
					bugs += [e[4] for e in inner].count('#')
				elif ex == 1: # left
					bugs += [e[0] for e in inner].count('#')
				continue
			#print('test',x+ex,y+ey)
				#print('bug',x+ex,y+ey)
		return bugs		

	def next_eris(eris,outer,inner):
		next_eris = []
		for y in range(len(eris)):
			eris_row = []
			for x in range(len(eris[y])):
				bugs = count_bugs(eris,x,y,outer,inner)
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


	def next_state(universe):
		universe_next = {}
		for idx, eris in universe.items():
			outer = None
			if idx-1 in universe:
				outer = universe[idx-1]
			inner = None
			if idx+1 in universe:
				inner = universe[idx+1]
			universe_next[idx] = next_eris(eris,outer,inner)
		# try to grow -1 and +1
		outmost_eris = new_outer_eris(universe[min(universe)])
		if sum([e.count('#') for e in outmost_eris])>0:
			universe_next[min(universe)-1]=outmost_eris

		inmost_eris = new_inner_eris(universe[max(universe)])
		if sum([e.count('#') for e in inmost_eris])>0:
			universe_next[max(universe)+1]=inmost_eris
		return universe_next		


	universe = {}
	universe[0]=eris
	for t in range(200):
		universe = next_state(universe)
		#print(t)
		# print_eris(universe[-1],'end[-1]')
		# print_eris(universe[0],'end[0]')
		# print_eris(universe[1],'end[1]')
	#print(sorted(universe.keys()))
	totbugs = sum([sum([row.count('#') for row in universe[e]]) for e in universe])
	return totbugs

eris = [list(t) for t in input]
eris[2][2] = '?'
#print_eris(eris,'start')

print('#2',part2(eris))



