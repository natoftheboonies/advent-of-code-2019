# https://github.com/metalim/metalim.adventofcode.2019.python/blob/master/18_vault_keys.ipynb

from collections import defaultdict
from itertools import count

with open('input') as file:
	input = file.read()

def parseInput(input):
	maze = {}
	goals = {}
	for y,row in enumerate(input.split('\n')):
		for x,cell in enumerate(row):
			p = complex(x,y)
			maze[p] = cell
			if cell in '#.': continue
			goals[cell] = p
	return maze, goals

def findLinks(maze, start):
	links = {}
	walk = defaultdict(lambda:[99999,{}])
	walk[start] = (0,set())
	next = [(start,set())]

	for step in count(1):
		if len(next)==0: break
		cur,next = next,[]
		for p,ds in cur:
			for d in [1,1j,-1,-1j]:
				c = maze[p+d]
				if c == '#' or walk[p+d][0]<=step: continue
				if c.islower():
					links[c] = (step,ds)
				nds = ds
				if c.isupper():
					nds = nds | {c.lower()}
				walk[p+d] = (step,nds)
				next.append((p+d,nds))
	return links # naturally sorted by distance

def part1():
	maze, goals = parseInput(input)

	allKeys = {k for k in goals if k.islower()}
	links = {'@': findLinks(maze, goals['@'])}
	for k in allKeys:
		links[k] = findLinks(maze, goals[k])

	cache = {}
	def walk(name, needKeys):
		if len(needKeys)==0:
			return 0

		key = name + ''.join(needKeys)
		if key in cache:
			return cache[key]

		shortest = float('inf')
		for k in needKeys:
			l,doors = links[name][k]
			if l >= shortest: continue # too long to try
			if not doors.isdisjoint(needKeys): continue # can't open doors
			tail = walk(k, needKeys - {k})
			if shortest > l + tail: shortest = l + tail
		cache[key] = shortest
		return shortest
	
	res = walk('@', allKeys)
	print('cached',len(cache))
	return res

def part2():
	maze, goals = parseInput(input)

	s = goals['@']
	maze[s]=maze[s+1]=maze[s-1]=maze[s+1j]=maze[s-1j]='#'
	maze[s+1+1j]='1'; goals['1'] = s+1+1j
	maze[s-1+1j]='2'; goals['2'] = s-1+1j
	maze[s+1-1j]='3'; goals['3'] = s+1-1j
	maze[s-1-1j]='4'; goals['4'] = s-1-1j

	allKeys = {k for k in goals if k.islower()}
	links = {}
	for k in '1234':
		links[k] = findLinks(maze, goals[k])
	for k in allKeys:
		links[k] = findLinks(maze, goals[k])

	cache = {}
	def walk(names, needKeys):
		if len(needKeys)==0:
			return 0

		key = ''.join(sorted(names)) + ''.join(sorted(needKeys))
		if key in cache:
			return cache[key]

		shortest = float('inf')
		for k in needKeys:
			for k2 in names:
				if k not in links[k2]: continue

				l,doors = links[k2][k]
				if l >= shortest: continue # too long to try
				if not doors.isdisjoint(needKeys): continue # can't open doors
				tail = walk((names - {k2}) | {k}, needKeys - {k})
				if shortest > l + tail: shortest = l + tail
		cache[key] = shortest
		return shortest
	
	res = walk({'1','2','3','4'}, allKeys)
	print('cached',len(cache))
	return res

if __name__ == '__main__':
	print('#1',part1())
	print('#2',part2())
