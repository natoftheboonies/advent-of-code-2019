infile = open('input1')
input = infile.readlines()
masses = map(int, input)
# fuel = floor(mass / 3)-2

#masses = [12, 14, 1069, 100756]
sum = 0
sumfuel = 0
for mass in masses:
	module_fuel = mass // 3 - 2
	moduel_fuel_fuel = 0
	sum += module_fuel
	addition = module_fuel
	while (addition // 3 - 2) > 0:
		addition_fuel = addition // 3 - 2
		moduel_fuel_fuel += addition_fuel
		addition = addition_fuel
	sumfuel += moduel_fuel_fuel


print('#1', sum) # 3457281
print ('#2', sum+sumfuel) #5183030

# 5185877 is too high
# 1728596 is too low


