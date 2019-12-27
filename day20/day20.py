from collections import defaultdict, deque

sample = '''         A           
         A           
  #######.#########  
  #######.........#  
  #######.#######.#  
  #######.#######.#  
  #######.#######.#  
  #####  B    ###.#  
BC...##  C    ###.#  
  ##.##       ###.#  
  ##...DE  F  ###.#  
  #####    G  ###.#  
  #########.#####.#  
DE..#######...###.#  
  #.#########.###.#  
FG..#########.....#  
  ###########.#####  
             Z       
             Z       
'''

input = sample.split('\n')

with open('input','r') as fp:
	input = fp.read().split('\n')
	pass

with open('sample2','r') as fp:
	#input = fp.read().split('\n')
	pass

right = len(input[3])
bottom = len(input)-1

print('range:',right,bottom)

maze = defaultdict(str)

hole_left = 1000
hole_right = 0
hole_top = 1000
hole_bottom = 0

for y,row in enumerate(input):
	for x,cell in enumerate(row):
		maze[(x,y)] = cell
		if x > 2 and x < right-2 and y > 2 and y < bottom-2 and cell==' ':
			hole_left = min(hole_left,x)
			hole_right = max(hole_right,x)
			hole_top = min(hole_top,y)
			hole_bottom = max(hole_bottom,y)
#print(maze)

print('hole:',hole_left,hole_top,'to',hole_right,hole_bottom)

portals = defaultdict(list)
# now let's find portals:
for y in range(2,bottom-1):
	if maze[(0,y)] != ' ':
		print(maze[(0,y)]+maze[(1,y)],'at',2,y)
		portals[maze[(0,y)]+maze[(1,y)]].append((2,y))
	if maze[right-1,y] != ' ':
		print(maze[(right-2,y)]+maze[(right-1,y)],'at',right-3,y)
		portals[maze[(right-2,y)]+maze[(right-1,y)]].append((right-3,y))
for x in range(2,right-1):
	if maze[(x,0)] != ' ':
		print(maze[(x,0)]+maze[(x,1)],'at',x,2)
		portals[maze[(x,0)]+maze[(x,1)]].append((x,2))
	if maze[(x,bottom-1)] != ' ':
		print(maze[(x,bottom-2)]+maze[(x,bottom-1)],'at',x,bottom-3)
		portals[maze[(x,bottom-2)]+maze[(x,bottom-1)]].append((x,bottom-3))	

#print('hole')
for y in range(hole_top,hole_bottom+1):
	if maze[(hole_left,y)] != ' ':
		print(maze[(hole_left,y)]+maze[(hole_left+1,y)],'at',hole_left-1,y)
		portals[maze[(hole_left,y)]+maze[(hole_left+1,y)]].append((hole_left-1,y))
	if maze[hole_right-1,y] != ' ':
		print(maze[(hole_right-1,y)]+maze[(hole_right,y)],'at',hole_right+1,y)
		portals[maze[(hole_right-1,y)]+maze[(hole_right,y)]].append((hole_right+1,y))

for x in range(hole_left,hole_right+1):
	if maze[(x,hole_top)] != ' ':
		print(maze[(x,hole_top)]+maze[(x,hole_top+1)],'at',x,hole_top-1)
		portals[maze[(x,hole_top)]+maze[(x,hole_top+1)]].append((x,hole_top-1))
	if maze[(x,hole_bottom)] != ' ':
		print(maze[(x,hole_bottom-1)]+maze[(x,hole_bottom)],'at',x,hole_bottom+1)
		portals[maze[(x,hole_bottom-1)]+maze[(x,hole_bottom)]].append((x,hole_bottom+1))

# let's check our portals
#print(portals)
assert len(portals['AA'])==1
assert len(portals['ZZ'])==1
for x in portals.keys():
	if x == 'AA' or x == 'ZZ':
		continue
	assert len(portals[x])==2

# now just some BFS stuff...
# https://pythoninwonderland.wordpress.com/2017/03/18/how-to-implement-breadth-first-search-in-python/

def find_neighbors(node):
	valid = []
	# if we are on a portal, warp
	for x in portals.keys():
		if x == 'AA' or x == 'ZZ':
			continue
		if portals[x][0]==node:
			valid.append(portals[x][1])
		elif portals[x][1]==node:
			valid.append(portals[x][0])
	#print("node",node)
	for move in (0,1),(0,-1),(1,0),(-1,0):
		check = (node[0]+move[0],node[1]+move[1])
		if maze[check] == '.':
			valid.append(check)

	return valid


def bfs_search(start,goal):
	explored = set()
	queue = [[start]]

	#print(queue)
	while queue:
		path = queue.pop(0)
		node = path[-1]
		if node not in explored:
			neighbors = find_neighbors(node)
			for neighbor in neighbors:
				new_path = list(path)
				new_path.append(neighbor)
				queue.append(new_path)
				#print(new_path)
				if neighbor == goal:
					#print('goal!', new_path)
					return new_path
			explored.add(node)
	return None

path = bfs_search(portals['AA'][0],portals['ZZ'][0])
print('#1',len(path)-1)
#1 600 :)


# and now, with depth!

def find_neighbors2(node): # node is [(x,y),d] where d is depth
	#print('node2',node)
	valid = []
	# if we are on a portal, warp
	for x in portals.keys():
		if x == 'AA' or x == 'ZZ':
			continue
		#print('node',node)
		if portals[x][0]==node[0] and node[1]>0:
			valid.append([portals[x][1],node[1]-1])
		elif portals[x][1]==node[0] and node[1]<=len(portals):
			valid.append([portals[x][0],node[1]+1])
	#print("node",node)
	for move in (0,1),(0,-1),(1,0),(-1,0):
		check = (node[0][0]+move[0],node[0][1]+move[1])
		if maze[check] == '.':
			valid.append([check,node[1]])

	return valid


def bfs_search2(start,goal):
	explored = set() # set needs flattened tuple
	queue = deque([[start]]) #[[start]]
	#print(queue)

	#print(queue)
	while queue:
		path = queue.popleft()
		#print(path)
		node = path[-1]
		if (node[0][0],node[0][1],node[1]) not in explored:
			neighbors = find_neighbors2(node)
			for neighbor in neighbors:
				new_path = list(path)
				new_path.append(neighbor)
				queue.append(new_path)
				#print(new_path)
				if neighbor == goal:
					#print('goal!', new_path)
					return new_path
			explored.add((node[0][0],node[0][1],node[1]))
	return None

path = bfs_search2([portals['AA'][0],0],[portals['ZZ'][0],0])

def printpath(path):
	count = 0
	for step in path:
		for x in portals.keys():
			if x == 'AA' or x == 'ZZ':
				continue
			if step[0] == portals[x][0] or step[0] == portals[x][1]:
				print(count,'steps to',x,step[1])
				count = 0
		count += 1
	print(count, 'steps to goal')

#printpath(path)
print('#2',len(path)-1)
#2 6666