import numpy as np
import random
import math
import operator
from operator import itemgetter

operators = {   "+": operator.add, 
				"-": operator.sub,
				"*": operator.mul,
				"%": operator.mod,
				"/": operator.truediv	
			}
				
				
inputs =  [0, 0.1,   0.2,  0.3,   0.4,  0.5,   0.6,  0.7,   0.8,  0.9]
outputs = [0, 0.005, 0.02, 0.045, 0.08, 0.125, 0.18, 0.245, 0.32, 0.405]

constant_numbers = [-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5]

terminals = [-54, -55]
functions = ["+", "-", "*", "%", "/"]

terminals_size = 1
functions_size = 1

n_population = 125

reproduction_prob = 0.1
mutation_prob = 0.1
crossover_prob = 0.8

individual_size = 7							#	(/(* x x)(/ 2 1))
function_pattern = [1, 1, 0, 0, 1, 0, 0]  	#	1 for function; 0 for terminal

k_adversaries = 10
crossover_point = 4

data = []

def get_random_terminal():
	tmp = random.randint(0, terminals_size)
	if( tmp == 0):
		return tmp
	else:
		rand_1 = random.randint(0, len(constant_numbers) - 1)
		return constant_numbers[rand_1]

def get_random_function():
	return random.randint(0, functions_size)
 
#Funcion para calcular el Fitness  	
def function_fitness( x ):
	MSE = 0.
	for i in range(len(inputs)):
		c_1 = inputs[i] if x[2]==-54 else x[2]
		c_2 = inputs[i] if x[3]==-54 else x[3]
		c_3 = inputs[i] if x[5]==-54 else x[5]
		c_4 = inputs[i] if x[6]==-54 else x[6]

		if( (functions[x[1]] == "/" or functions[x[1]] == "%") and c_2 == 0):
			a = 0.
		else:
			a = operators[functions[x[1]]] ( c_1, c_2)
			
		if( (functions[x[4]] == "/" or functions[x[4]] == "%") and c_4 == 0):
			b = 0.
		else:
			b = operators[functions[x[4]]] ( c_3, c_4)
			
		if( (functions[x[0]] == "/" or functions[x[0]] == "%") and b == 0):
			c = 0
		else:
			c = operators[functions[x[0]]] (a, b)
			
		MSE += abs( outputs[i] - c )**2
	return  MSE / len(inputs)


def generate_population(n_population, individual_size):
	population = []
	for i in range(n_population):
		tmp_function = []
		for j in function_pattern:
			if( j == 1):
				tmp_function.append(get_random_function())
			else:
				tmp_function.append(get_random_terminal())
		population.append(tmp_function)
	print("Generando Poblacion:")
	print('\n'.join(' '.join(map(str,i)) for i in population))
	for i in population:
		data.append([i, [0] ])
	print_symbols()

def eval_population():

	for i in data:
		i[1][0] = ( function_fitness( i[0] ) )

def print_symbols_one(i):

	for j, k in zip(i[0], function_pattern):
		if( k == 1 ):
			print(functions[j], end='  ')
		else:
			if(j == 0):
				print('x', end='  ')
			else:
				print(j, end='  ')
	print("\t"+str( i[1]) )


def print_symbols():
	for i in data:
		for j, k in zip(i[0], function_pattern):
			if( k == 1 ):
				print(functions[j], end='  ')
			else:
				if(j == 0):
					print('x', end='  ')
				else:
					print(j, end='  ')
		print("\t"+str( i[1]) )

#Seleccion por torneto de elementos de la poblacion tomando como ganador el que tenga el mejor fitness
def get_parent(k_adversaries):
	pool = len(data)
	selected = []

	for i in range(k_adversaries):
		tmp = random.randint(0, pool-1)
		selected.append([tmp, data[tmp][1]])

	index, value = min(enumerate([i[1] for i in selected]), key=itemgetter(1))
	parent_index = selected[index][0]
	return parent_index


def tournament_selection(k_adversaries):
	return get_parent(k_adversaries)

#Cruzamiento punto a punto
def crossover( parent_index_1, parent_index_2 ):
	offpsring = []

	crossover_point = random.randint(1, individual_size-2)

	mother_cromosome = data[parent_index_1][0]
	father_cromosome = data[parent_index_2][0]

	son_1 = np.concatenate([mother_cromosome[0:crossover_point], \
						father_cromosome[crossover_point:]])
	son_2 = np.concatenate([father_cromosome[0:crossover_point], \
						mother_cromosome[crossover_point:]])

	offpsring.append(list(son_1))
	offpsring.append(list(son_2))
	return offpsring

#Mutacion 
def mutation( parent_index ):
	random_index = random.randint(0, individual_size-1)
	tmp = list(data[parent_index][0])
	if( function_pattern[random_index] ):
		tmp[random_index] = get_random_function()
	else:
		tmp[random_index] = get_random_terminal()
	return tmp



#Reducimos la población mantieniendo a los de mejor fitnes
def sorting_population():
	global data
	tmp = []
	for i,x in zip(data,range(len(data))):
		tmp.append([x, i[1]])
	
	tmp = sorted(tmp, key=itemgetter(1), reverse=False) #Ordenacion
	ms = []

	for i in range(n_population):
		ms.append(data[tmp[i][0]])
	data = ms

def genetic_programing():
	#Generación de población
	generate_population(n_population, individual_size)
	#Evaluación de población
	eval_population()
	global data
	
	L2 = (crossover_prob + reproduction_prob)
	tol = 1e-12
	counter = 0
	
	while(True):
		pass
		print("iteration: ", counter)

		tmp = []
		while(True):
			if( len(tmp) >= n_population ):
				break
			genetic_operation = random.uniform(0, 1)
			if(genetic_operation <= crossover_prob):
				#Cruzamiento
				print("Cruzamiento")
				parent_1 = tournament_selection(k_adversaries)
				
				print("Padre 1", end=" : ")
				print_symbols_one(data[parent_1])
				
				parent_2 = tournament_selection(k_adversaries)
				
				print("Padre 2" , end=" : ")
				print_symbols_one(data[parent_2])
				
				offspring = crossover(parent_1, parent_2)
				
				#Desendientes				
				for i in offspring:
					newSon = [i, [function_fitness(i)]]
					tmp.append(newSon)
					print("Desendiente " , end=" : ")
					print_symbols_one(newSon)
				print("--------------------\n")
					
					
					
			elif( crossover_prob < genetic_operation <= L2):
				#Reproduction
				print("\nReproduccion")
				parent_1 = tournament_selection(k_adversaries)
				print("Padre e hijo ", end=" : ")
				print_symbols_one(data[parent_1])
				print("---------------------------\n")
				
				tmp.append(data[parent_1])
				
			elif( L2 < genetic_operation <= 1.0 ):
				#Mutación
				print("\nMutacion")
				parent_1 = tournament_selection(k_adversaries)
				
				print("Individuo", end=" : ")
				print_symbols_one(data[parent_1])
				son = mutation(parent_1)
				newSon = [ son, [function_fitness(son)]]
				tmp.append(newSon)
				print("Individuo Mutado " ,end=" : ")
				print_symbols_one(newSon)
				print("-----------------------\n")

		del data
		data = []


		
		for i in tmp:
			data.append(i)
		
		tmp = []
		for i,x in zip(data,range(len(data))):
			tmp.append([x, i[1]])
		
		tmp = sorted(tmp, key=itemgetter(1), reverse=False) #Ordenacion
		ms = []

		for i in range(n_population):
			ms.append(data[tmp[i][0]])
		data = ms


		counter+=1
		sorting_population()
		if (data[0][1][0] < tol or counter == 100):
			break

	print("RESULTS")
	print_symbols()

genetic_programing()


