from math import gcd

def calculate_energy(moons, duration):
	moonv = [[0,0,0] for moon in moons]

	time = 0

	while time < duration:
		time += 1
		for i in range(len(moons)):
			for j in range(i+1,len(moons)):
				#print('compare',i,j)
				# update velocity
				for c in range(3):
					if moons[i][c] > moons[j][c]:
						moonv[i][c]-=1
						moonv[j][c]+=1
					elif moons[i][c] < moons[j][c]:
						moonv[j][c]-=1
						moonv[i][c]+=1
		# update position
		for i in range(len(moons)):
			for c in range(3):
				moons[i][c]+=moonv[i][c]

	total_energy = 0
	for i in range(len(moons)):
		potential = sum([abs(x) for x in moons[i]])
		kinetic = sum([abs(x) for x in moonv[i]])
		#print(potential,'x',kinetic)
		total_energy += potential*kinetic
	return total_energy


def parse_moons(lines):
	moons = []
	#moonv = []
	for line in lines:
		inp = line.strip().split(',')
		x = inp[0][inp[0].index('=')+1:]
		y = inp[1][inp[1].index('=')+1:]
		z = inp[2][inp[2].index('=')+1:len(inp[2])-1]
		moons.append([int(x),int(y),int(z)])
		#moonv.append([0,0,0])	
	return moons

def find_period(moons):
	moonv = [[0,0,0] for moon in moons]

	time = 0
	period = [0, 0, 0]

	while time < 1000000:
		time += 1
		for i in range(len(moons)):
			for j in range(i+1,len(moons)):
				#print('compare',i,j)
				# update velocity
				for c in range(3):
					if moons[i][c] > moons[j][c]:
						moonv[i][c]-=1
						moonv[j][c]+=1
					elif moons[i][c] < moons[j][c]:
						moonv[j][c]-=1
						moonv[i][c]+=1
		# update position
		for i in range(len(moons)):
			for c in range(3):
				moons[i][c]+=moonv[i][c]

		found = [True,True,True]
		for i in range(len(moons)):
			for c in range(3):
				if moonv[i][c]!=0:
					found[c] = False
		for c in range(3):	
			if found[c] and period[c] == 0:	
				period[c] = time

		if period[0] > 0 and period[1] > 0 and period[2] > 0:
			return period

# https://stackoverflow.com/questions/37237954/calculate-the-lcm-of-a-list-of-given-numbers-in-python
def lcm(period):
	lcm = period[0]
	for i in period[1:]:
		lcm = int(lcm*i/gcd(lcm, i))
	return lcm*2


sample = '''<x=-1, y=0, z=2>
<x=2, y=-10, z=-7>
<x=4, y=-8, z=8>
<x=3, y=5, z=-1>'''

moons = parse_moons(sample.split('\n'))
assert calculate_energy(moons,10)==179

sample2 = '''<x=-8, y=-10, z=0>
<x=5, y=5, z=10>
<x=2, y=-7, z=3>
<x=9, y=-8, z=-3>'''

moons = parse_moons(sample2.split('\n'))
assert calculate_energy(moons,100)==1940

lines = None
with open('input') as fp:
	lines = fp.readlines()

moons = parse_moons(lines)
print('#1',calculate_energy(moons,1000))

# part 2, find repeating

moons = parse_moons(sample.split('\n'))
period = find_period(moons)
assert lcm(period)==2772


moons = parse_moons(sample2.split('\n'))
period = find_period(moons)
#print(period, period[0]*period[1]*period[2])
assert lcm(period)==4686774924


moons = parse_moons(lines)
period = find_period(moons)
print(period)
print('#2',lcm(period))








