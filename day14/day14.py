from collections import defaultdict, deque
import re
from math import ceil
formula = {}

def parse_reactions(lines):
	reactions = {}
	#moonv = []
	for line in lines:
		if len(line) == 0:
			continue
		inp = line.strip().split('=')
		out = inp[1][2:].split(' ')
		out = tuple([int(out[0]),out[1]])
		#print(out[1],'needs',out[0])
		inp = [x.strip().split(' ') for x in inp[0].split(',')]
		inp = [tuple([int(x[0]),x[1]]) for x in inp]
		#print(inp)
		# e.g., 5 B, 7 C => 1 BC:
		# 'BC' : 1, [(5, 'B'), (7, 'C')]
		reactions[out[1]] = (out[0],inp)

	return reactions


def calculate_fuel():
	#global formula
	need = deque([(1,'FUEL')])
	excess = defaultdict(int)

	ore = 0
	
	while need:
		# turn a need into the parts and excesses
		qty, what = need.popleft()
		if what == 'ORE':
			print(f'need {qty} {what}')
			ore += qty
			continue
		print('need',qty,what)

		# use up excess
		if excess[what] >= qty:
			excess[what] -= qty
			continue
		else: #qty < excess
			qty -= excess[what]
			excess[what] = 0


		formula_qty, stuff = formula[what] # FUEL = 1, [(7, 'B'), (1, 'E')]

		mult = ceil(qty/formula_qty) # e.g., if need 14, recipe 10, then 2x
		print('and thats',mult, 'times',stuff)

		for y in stuff:
			amt = y[0]*mult 
			chem = y[1]
			print('add', amt, chem)
			need.append((amt, chem))
		
		produced_qty = formula_qty * mult
		excess[what] += (produced_qty - qty)

		print('state',need)
		print('excess',excess)
	print('#1',ore)


sample = '''10 ORE => 10 A
1 ORE => 1 B
7 A, 1 B => 1 C
7 A, 1 C => 1 D
7 A, 1 D => 1 E
7 A, 1 E => 1 FUEL'''

'''
need = 1F
have = 0
---
1F = 7A,1E
need = 7A, 1E
have =
---
need = 10 ORE, 7A, 1D
have = 3A
---
need = 10 ORE, 10 ORE, 7A, 1C
have = 3A, 3A
---
need = 10 ORE, 10 ORE, 10 ORE, 7A, 1B
have = 3A, 3A, 3A
---
need = 10 ORE, 10 ORE, 10 ORE, 1 ORE
have = 2A

1F = 7A,7A,1D
1F = 7A,7A,7A,7C
1F = 7A,7A,7A,7A,1B
1F = 28A, 1B

'''

sample = '''9 ORE => 2 A
8 ORE => 3 B
7 ORE => 5 C
3 A, 4 B => 1 AB
5 B, 7 C => 1 BC
4 C, 1 A => 1 CA
2 AB, 3 BC, 4 CA => 1 FUEL'''

sample = '''157 ORE => 5 NZVS
165 ORE => 6 DCFZ
44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL
12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ
179 ORE => 7 PSHF
177 ORE => 5 HKGWZ
7 DCFZ, 7 PSHF => 2 XJWVT
165 ORE => 2 GPVTF
3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT'''

with open('input') as fp:
	sample = fp.read()

formula = parse_reactions(sample.split('\n'))
#print('rs',reactions)
calculate_fuel()
#print(formula['FUEL'])
