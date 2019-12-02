import pandas as pd

data = pd.read_csv('warmup-input')
print(data)

input = '1111'
last = ''
result = 0
print(input)
for x in range(len(input)):
	if input[x]==last:
		result+=int(last)
	last = input[x]
	#print(input[x])
if input[0]==last:
	result+=int(last)

print("result:",result)