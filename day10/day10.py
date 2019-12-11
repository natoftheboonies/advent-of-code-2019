#from functools import cmp_to_key

program = []
with open('input', 'r') as infile:
	inprog = '''.#..#
.....
#####
....#
...##'''.splitlines()
	inprog = infile.readlines()
	for i in inprog:
		#print(i)
		program.append(list(i.strip()))

def gcd(a,b): 
	a = abs(a)
	b = abs(b)        
	if (a == 0): 
		return b 
	if (b == 0): 
		return a 

	# base case 
	if (a == b): 
		return a 

	# a is greater 
	if (a > b): 
		return gcd(a-b, b) 
	return gcd(a, b-a) 

asteroids = {}
for y in range(len(program)):
	for x in range(len(program[y])):
		if program[y][x]=='#':
			#print(f'asteroid at {x},{y}')
			asteroids[(x,y)]={}

for ast in asteroids.keys():
	targets = {} # directions : [(dist, oth)]
	for oth in asteroids.keys():
		if ast==oth:
			continue
		# what direction is oth from ast?
		so = (oth[0]-ast[0],oth[1]-ast[1])
		# how far away is oth from ast?
		then = gcd(so[0],so[1])
		# reduce direction by distance
		so = (so[0]//then,so[1]//then)
		# now check
		if so not in targets.keys():
			targets[so] = []
		targets[so].append((then,oth))
	asteroids[ast] = targets

station = None
count = 0
for ast in asteroids.keys():
	#print(ast,len(asteroids[ast]))
	if len(asteroids[ast])>count:
		count = len(asteroids[ast])
		station = ast

print('#1',station,count)

targets = asteroids[station]
# sort by clockwise? hmmm...
# https://stackoverflow.com/questions/6989100/sort-points-in-clockwise-order
# bah this didn't work
def cmp(a, b):
	if a[0]>=0 and b[0]<0:
		return True
	if a[0]<0 and b[0]>=0:
		return False
	if a[0]==0 and b[0]==0:
		if a[1]>=0 and b[1]>=0:
			return a[1]>b[1]
		return b[1]>a[1]
	det = a[0]*b[1]-b[0]*a[1]
	if det<0:
		return True
	if det>0:
		return False
	d1 = a[0]**2+a[1]**2
	d2 = b[0]**2+b[1]**2
	return d1>d2

#dirs = [(0,-1),(1,0),(0,1),(-1,0)]
q1targ = [t for t in targets.keys() if t[0]>=0 and t[1]<0]
q2targ = [t for t in targets.keys() if t[0]>=0 and t[1]>=0]
q3targ = [t for t in targets.keys() if t[0]<0 and t[1]>=0]
q4targ = [t for t in targets.keys() if t[0]<0 and t[1]<0]
print('targets per quadrant',len(q1targ),len(q2targ),len(q3targ),len(q4targ))
# 34,12,52,182 so #200 in q4

q4sort = sorted(q4targ,key=lambda t:t[1]/t[0]) # aha! sort by slope!

# ok just hardcode targets per quadrant to figure how far in q4sort
x=199-12-34-52

#print(q4sort[x],'>>>',targets[q4sort[x]])
shoot = targets[q4sort[x]][0][1]
print('#2',shoot[0]*100+shoot[1])


#directions = sorted(targets.keys(),key=cmp_to_key(cmp))
#print(directions[0:5], len(directions))

