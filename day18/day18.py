from collections import defaultdict, deque

sample = '''#########
#b.A.@.a#
#########
'''

sample2 = '''########################
#f.D.E.e.C.b.A.@.a.B.c.#
######################.#
#d.....................#
########################
'''

sample2 = '''########################
#...............b.C.D.f#
#.######################
#.....@.a.B.c.d.A.e.F.g#
########################
'''

sample2 = '''########################
#@..............ac.GI.b#
###d#e#f################
###A#B#C################
###g#h#i################
########################
'''

sample2 = '''#################
#i.G..c...e..H.p#
########.########
#j.A..b...f..D.o#
########@########
#k.E..a...g..B.n#
########.########
#l.F..d...h..C.m#
#################
'''

maze = defaultdict(str)

lines = sample.split('\n')
with open('input') as fp:
	#lines = fp.readlines()
	pass

start = None
allkeys = set()
for y, line in enumerate(lines):
	for x, char in enumerate(line):
		maze[x,y]=char
		if char == '@':
			start = (x,y)
		elif char.islower():
			allkeys.add(char)

print(start, allkeys)


def find_neighbors(node): # node is [(x,y),k] where k is keys
	pos = node[0]
	keys = node[1]
	valid = []
	for move in (0,1),(0,-1),(1,0),(-1,0):
		check = (pos[0]+move[0],pos[1]+move[1])
		#print('checking',maze[check])
		if maze[check] in '.@' or (maze[check].isupper() and maze[check].lower() in keys):
			valid.append([check,keys])
			#print('check',check,keys)
		elif maze[check].islower():
			new_keys = set(keys)
			new_keys.add(maze[check])
			valid.append([check,new_keys])
			#print('check2',check,keys)
	return valid

def flatten(node):
	return tuple([node[0][0],node[0][1]]+list(sorted(node[1])))

def bfs_search(start):
	explored = set() # set needs flattened tuple
	queue = deque([[start]]) #[[start]]
	while queue:
		path = queue.popleft()
		#print(path)
		node = path[-1]
		if flatten(node) not in explored:
			neighbors = find_neighbors(node)
			for neighbor in neighbors:
				new_path = list(path)
				new_path.append(neighbor)
				queue.append(new_path)
				#print(new_path)
				if neighbor[1] == allkeys:
					#print('goal!', new_path)
					return new_path

			explored.add(flatten(node))
	return None

path = bfs_search([start,set()])
#print(path)
print('#1',len(path)-1)
#1 4544
#[Finished in 91.7s]