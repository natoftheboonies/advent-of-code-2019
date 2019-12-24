

# deal into new stack
#sample.reverse()
#print(sample)

def deal_new(stack):
	new_stack = stack[:]
	new_stack.reverse()
	return new_stack

def deal(stack, inc):
	new_stack = stack[:]
	y = 0
	for x in range(0,len(stack)*inc,inc):
		new_stack[x%len(stack)] = stack[y]
		y+=1	
	return new_stack

def cut(stack, top):
	return stack[top:]+stack[:top]

sample = list(range(10))

assert deal_new(sample) == [9,8,7,6,5,4,3,2,1,0]
assert deal(sample,3) == [0,7,4,1,8,5,2,9,6,3]
assert cut(sample,3) == [3,4,5,6,7,8,9,0,1,2]
assert cut(sample,-4) == [6,7,8,9,0,1,2,3,4,5]




def follow(inst,deck):
	for t in inst:
		#print(t)
		if t.startswith('deal with'):
			inc = int(t[20:])
			#print('deal',inc)
			deck = deal(deck,inc)
		elif t.startswith('cut'):
			top=int(t[4:])
			#print('cut',top)
			deck = cut(deck,top)
		elif t.startswith('deal into'):
			#print('deal_new')
			deck = deal_new(deck)
		else:
			print('unknown instruction')
	return deck

inst = '''deal with increment 7
deal with increment 9
cut -2
'''.strip().split('\n')

assert follow(inst,list(range(10)))==[6,3,0,7,4,1,8,5,2,9]

inst = '''deal into new stack
cut -2
deal with increment 7
cut 8
cut -4
deal with increment 7
cut 3
deal with increment 9
deal with increment 3
cut -1
'''.strip().split('\n')

assert follow(inst,list(range(10)))==[9,2,5,8,1,4,7,0,3,6]

inst = None
with open('input','r') as fp:
	inst = fp.read().strip().split('\n')

result = follow(inst,list(range(10007)))
print('#1',result.index(2019))
#1 6431

