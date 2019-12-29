input = None
with open('input','rt') as fp:
	input = fp.read().strip()

base_pattern = [0,1,0,-1]

def calc_phase(signal):
	phase = [0]*len(signal)
	#print(phase)
	for t in range(1,len(signal)+1):
		#patt_exp = [[s]*t for s in base_pattern]
		#pattern = [t for sub in patt_exp for t in sub]
		pattern = base_pattern
		#print(pattern)
		calc = 0
		for p in range(t-1,len(signal)):
			# skip the *0 ones?
			#if (p+1)//t==2:
			#	continue
			#if t==1:
			#	print('+',signal[p],'*',pattern[(p+1)%len(pattern)]) 
			calc += signal[p]*pattern[(p+1)//t%len(pattern)]
		phase[t-1] = (abs(calc)%10)
	return phase


def calc_rounds(signal, rounds):
	signal = list(map(int,list(signal)))
	for _ in range(rounds):
		signal = calc_phase(signal)
	return ''.join(map(str,signal))


assert calc_rounds('12345678',4) =='01029498'

assert calc_rounds('80871224585914546619083218645595',100)[:8]=='24176176'
assert calc_rounds('19617804207202209144916044189917',100)[:8]=='73745418'
assert calc_rounds('69317163492948606335995924319873',100)[:8]=='52432133'

print('#1',calc_rounds(input,100)[:8])
#1 74369033
#[Finished in 12.7s]

offset = int(input[:7])
#print(offset)

signal = list(map(int,list(input)))
signal = (signal*10000)[offset:]

for _ in range(100):
	for i in range(len(signal)-1, 0, -1): # go backwards, sez reddit
		signal[i-1] = (signal[i-1] + signal[i]) % 10
print('#2',''.join(map(str, signal[:8])))
#2 19903864
#[Finished in 16.0s]
