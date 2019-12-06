# orbits!

sample = '''COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L
K)YOU
I)SAN'''

orbitmap = {}
with open('input', 'r') as infile:
	input = [line.strip() for line in infile.readlines()]
	#input = sample.split('\n')
	orbitmap = {o.split(')')[1] : o.split(')')[0] for o in input}

count = 0
for orbit in orbitmap.keys():
	#print(f'{orbit} orbits {orbitmap[orbit]}')
	body = orbitmap[orbit]
	count+=1
	while body in orbitmap.keys():
		#print(f'{body} orbits {orbitmap[body]}')
		body = orbitmap[body]
		count+=1
print("#1", count)
#woohoo! 247089

body = orbitmap['YOU']
you_orbits = [body]
#print(f'YOU orbits {body}')
while body in orbitmap.keys():
	#print(f'{body} orbits {orbitmap[body]}')
	body = orbitmap[body]
	you_orbits.append(body)
#print(you_orbits)

body = orbitmap['SAN']
san_orbits = [body]
#print(f'SAN orbits {body}')
while body in orbitmap.keys():
	#print(f'{body} orbits {orbitmap[body]}')
	body = orbitmap[body]
	san_orbits.append(body)
#print(san_orbits)

common = [body for body in san_orbits if body in you_orbits][0]
#print(common)
#print('you',you_orbits.index(common))
#print('san',san_orbits.index(common))

print ('#2', you_orbits.index(common)+san_orbits.index(common))

