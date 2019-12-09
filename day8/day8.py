program = []
with open('input', 'r') as infile:
	inprog = '123456789012' # 3x2
	inprog = infile.readline().strip()	
	input = list(inprog)
	program = list(map(int,input))

#print(program)

x, y = 3, 2
x, y = 25, 6

layers = []
zeros = None
result = None
for i in range(0, len(program), x*y):
	layer = program[i:i+x*y]
	if not zeros or layer.count(0) < zeros:
		zeros = layer.count(0)
		result = layer.count(1)*layer.count(2)
	layers.append(layer)

print('#1',result)

img = [2]*(x*y)
for i in range(x*y):
	for j in range(len(layers)):
		if layers[j][i]==2:
			continue
		img[i] = layers[j][i]
		break

print('#2')
for i in range(0, len(img), x):
	print(''.join(['*' if t == 1 else ' ' for t in img[i:i+x]]))

