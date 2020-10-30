

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

# i don't want to learn this math
# https://www.reddit.com/r/adventofcode/comments/ee0rqi/2019_day_22_solutions/fbwpk5k/
# didn't work ^^^
# https://github.com/metalim/metalim.adventofcode.2019.python/blob/master/22_cards_shuffle.ipynb

n = 119315717514047
c = 2020

M = 101741582076661

# convert rules to linear polynomial.
# (g∘f)(x) = g(f(x))
def parse(L, rules):
    a,b = 1,0
    for s in rules[::-1]:
        if s == 'deal into new stack':
            a = -a
            b = L-b-1
            continue
        if s.startswith('cut'):
            n = int(s.split(' ')[1])
            b = (b+n)%L
            continue
        if s.startswith('deal with increment'):
            n = int(s.split(' ')[3])
            z = pow(n,L-2,L) # == modinv(n,L)
            a = a*z % L
            b = b*z % L
            continue
        raise Exception('unknown rule', s)
    return a,b

# modpow the polynomial: (ax+b)^m % n
# f(x) = ax+b
# g(x) = cx+d
# f^2(x) = a(ax+b)+b = aax + ab+b
# f(g(x)) = a(cx+d)+b = acx + ad+b
def polypow(a,b,m,n):
    if m==0:
        return 1,0
    if m%2==0:
        return polypow(a*a%n, (a*b+b)%n, m//2, n)
    else:
        c,d = polypow(a,b,m-1,n)
        return a*c%n, (a*d+b)%n

def shuffle2(L, N, pos, rules):
    a,b = parse(L,rules)
    a,b = polypow(a,b,N,L)
    return (pos*a+b)%L

print('#2',shuffle2(n,M,c,inst))

