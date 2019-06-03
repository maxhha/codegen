import gene
from math import ceil
from sys import exit

print("""
==========================================
|        Brainf*ck code generator. V1    |
|        Author: Alexander Degtyarev     |
==========================================
   
   This program generates Brainf*ck code that copies value from first cell in memory to last one.
   Generation bases on genetic algorithm that minimises absolute error and code length.
   First, enter generation parameters. Then the generation will start.
   
   While enter values you can write "q" to exit.
""")

def input_int(text, default):
	while True:
		s = input("%s (default = %d ): " % (text, default))
		if s == "":
			print("Choosed default value")
			return default
		if s == "q":
			exit()
		i = None
		try:
			i = int(eval(s))
		except:
			print("Error while converting to integer")
			continue
		print("Entered %d" % i)
		return i

number_genes = input_int("Number of genes", 50)
number_epochs = input_int("Number of epochs", 100)
number_mutation = input_int("Number of mutations per one epoch", 25)
number_clones = input_int("Number of clones", 20)

NUMBER_PROGRESS_BARS = 13

mem_size = input_int("Brainf*ck memory size", 2)

epoch_show = int(number_epochs / 10)

X = list(range(1, 101, 5))
Y = X

def get_error(g):
	error = 0
	for x, y in zip(X, Y):
		pred_y = g.run(output_size=1, data=[x])[0]
		error += abs(pred_y - y)
	return error

gens = []

min_code_len = 0
check_continue = True

print("Start generation...")

for epoch in range(1, number_epochs+1):
	if len(gens) == 0:
		#Init first epoch
		gens = [gene.Gene(mem_size=mem_size).mutate(number_mutation) for i in range(number_genes)]
	else:
		#mutate last epoch
		gens = gens[:ceil(number_genes/number_clones)]
		for i in range(len(gens)):
			for _ in range(number_clones - 1):
				gens.append(gens[i].clone().mutate(number_mutation))
		gens = gens[:number_genes]
	#calculate errors and sort by error value then by code length
	a = list(enumerate(map(get_error, gens)))
	a.sort(key=lambda x: x[1])
	
	s = 0
	for i in range(len(a)):
		if a[i][1] != a[s][1]:
			b = a[s:i]
			b.sort(key=lambda x: len(gens[x[0]].code))
			a = a[:s] + b + a[i:]
			s = i
	
	gens = list(map(lambda x: gens[x[0]], a))
	error = a[0][1]
	k = int(epoch % epoch_show / epoch_show * NUMBER_PROGRESS_BARS)
	print("\r[->"+"+"*k + " "*(NUMBER_PROGRESS_BARS - k) + "<]", end="")
	if epoch % epoch_show == 0:
		print("\rEpoch %d; Error: %d" % (epoch, error))
	if error == 0 and (check_continue or min_code_len > len(gens[0].code)):
		min_code_len = len(gens[0].code)
		check_continue = False
		print("\rPerfect error = %d " % get_error(gens[0]))
		print("Perfect code is: \n" + gens[0].code)
		if not "y" in input("Continue? (y/N): "):
			break
			
print("\r==========================================")
print("Perfect error = %d " % get_error(gens[0]))
print("Perfect code is: \n" + gens[0].code)