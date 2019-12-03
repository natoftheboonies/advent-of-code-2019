
def printgrid(grid):
	for x in range(len(grid)):
		print(grid[x])

# https://stackoverflow.com/questions/563198/how-do-you-detect-where-two-line-segments-intersect
def doesntwork(seg,seg2):
	A = seg[0]
	B = seg[1]
	C = seg2[0]
	D = seg2[1]
	E = B[0]-A[0],B[1]-A[1]
	F = D[0]-C[0],D[1]-C[1]
	P = -1*E[1],E[0]
	hAminusC = A[0]-C[0],A[1]-C[1]
	hAmCxP = hAminusC[0]*P[0]+hAminusC[1]*P[1]
	hFxP = F[0]*P[0]+F[1]*P[1]
	h = hAmCxP/hFxP if hFxP > 0 else -1
	if h>=0 and h <=1:
		print ("cross",seg,seg2)
		cross =C[0]+F[0]*h,C[1]+F[1]*h
		print ("at", cross)

wire = []
with open('input', 'r') as infile:
	wire.append(infile.readline().strip().split(','))
	wire.append(infile.readline().strip().split(','))
	
	# sample 1
	#wire.append('R8,U5,L5,D3'.split(','))
	#wire.append('U7,R6,D4,L4'.split(','))

	# sample 2
	#wire.append('R75,D30,R83,U83,L12,D49,R71,U7,L72'.split(','))
	#wire.append('U62,R66,U55,R34,D71,R55,D58,R83'.split(','))

	# sample 3
	#wire.append('R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51'.split(','))
	#wire.append('U98,R91,D20,R16,D67,R40,U7,R15,U6,R7'.split(','))
	for i in range(len(wire)):
		wire[i]=[[inst[0],int(inst[1:])] for inst in wire[i]] 

#print(wire)

wirepoints = []

# let's try updating each point with a (x,y) point
for i in range(len(wire)):
	loc = [0,0]
	# and a list of all the points!
	dumb = dict()
	stepcount = 0
	for j in range(len(wire[i])):
		d, l = wire[i][j]
		#print(d,l)
		x = 0
		y = 0		
		if d == 'L':
			x = -1
		elif d == 'R':
			x = 1
		elif d == 'U':
			y = 1
		elif d == 'D':
			y = -1
		else:
			print("unexpected direction", d)			
		#loc = loc[0]+=x*l, loc[1]+=y*l
		for step in range(l):
			loc=loc[0]+x,loc[1]+y
			stepcount+=1
			dumb[loc] = stepcount
		wire[i][j].append(list(loc))
	wirepoints.append(dumb)

# no, cuz that's only corners :(  
# but we can calculate a grid, anyway!

#print(wire[0])
#print(wire[1])
xRange = min(loc[2][0] for loc in wire[0]+wire[1]), max(loc[2][0] for loc in wire[0]+wire[1])
yRange = min(loc[2][1] for loc in wire[0]+wire[1]), max(loc[2][1] for loc in wire[0]+wire[1])
print ('gridrange', xRange, yRange) # sample stays positive, input goes negative (of course)

intersections = wirepoints[0].keys() & wirepoints[1].keys()
print("intersections", intersections)
print("#1:",min(abs(x)+abs(y) for x,y in intersections))

for sect in intersections:
	blah = wirepoints[0][sect]+wirepoints[1][sect]
	print ("sect",sect,blah)

num2 = min(wirepoints[0][sect]+wirepoints[1][sect] for sect in intersections)
print ("#2:",num2)


# instead, let's try equations for each line? no, we have segments. 
# let's loop and check for intersections
for i in range(len(wire[0])):
	seg = [0,0] if i == 0 else wire[0][i-1][2], wire[0][i][2]
	#rint('seg',seg)
	for j in range(len(wire[1])):
		seg2 = [0,0] if j == 0 else wire[1][j-1][2], wire[1][j][2]
		
		#print('seg2',seg2)
		# https://www.geeksforgeeks.org/check-if-two-given-line-segments-intersect/
		# eh that's too hard.  let's just expand the lines into points, since square
		# https://stackoverflow.com/questions/563198/how-do-you-detect-where-two-line-segments-intersect
		# that doens't seem to work either.
		#doesntwork(seg,seg2)
		# ok just expand the lines
		

# yes this would be much more tidy if I deleted all my failed attempts. :-D



# too slow to allocate a grid to draw it
# https://stackoverflow.com/questions/2397141/how-to-initialize-a-two-dimensional-array-in-python
#grid = [x[:] for x in [[0]*(yRange[1]-yRange[0])]*(xRange[1]-xRange[0])]

#printgrid(grid)

# ok, now where to put the port? (0,0) but offset if we went negative...
#port = [0-xRange[0],0-yRange[0]]
#print('port:',port)
