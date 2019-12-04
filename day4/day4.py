# passwords!

criteria = (125730,579381)
#criteria = (142,396)

# enumerate passwords

def testpass(x, part2=False):
	t = x
	last = 0
	last_last = 0
	doubles = set()
	for y in (100000, 10000, 1000, 100, 10, 1): #100000, 10000, 1000,
		#print(t,y,last,last_last)
		if t//y<last:
			break
		if t//y==last:
			doubles.add(last)
			if part2 and t//y==last_last:
				#print ('triple',last, x)
				doubles.remove(last)
		last_last = last
		last = t//y
		t = t%y
	else:	
		if len(doubles) > 0:
			#print (doubles)
			return True
	return False


assert testpass(111122)
assert testpass(223333)

count = 0
for x in range(criteria[0],criteria[1]):
	if testpass(x):
		count+=1
	

print ("#1", count)

count = 0
for x in range(criteria[0],criteria[1]):
	if testpass(x, True):
		count+=1

print ("#2", count)
# for #2, 1015 too low... oh, cuz double that is not triple still good.