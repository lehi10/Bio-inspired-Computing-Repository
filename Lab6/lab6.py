import math
import random
import numpy as np


#optimization limits
x_lower_limit = -10.
x_upper_limit = 10.

#standard deviation
deviation = .3 # 1.0 0.5

individual_size = 2
population_size = 10
n_competitors = 3
n_iterations = 100

infinite = -1.

lim_inf = -4
lim_sup = 4
delta = 0.01

data = list()


def fitness_function( x_1, x_2):
	return -math.cos(x_1)*math.cos(x_2)*math.exp(-(x_1-math.pi)**2-(x_2-math.pi)**2)



def generate_individual( size, min_limit, max_limit ):
	xt = [ random.uniform(min_limit, max_limit) for i in range(size)]
	dev = [deviation]* individual_size
	fit = np.inf
	individual = {"xt":xt ,"dev": dev,"fit":fit }
	return individual


def generate_population( population_size ):
	for i in range( population_size ):
		data.append( generate_individual( individual_size, x_lower_limit, x_upper_limit) )


def evaluate_population():
	for ind in data:
		ind["fit"] = fitness_function( ind["xt"][0], ind["xt"][1] )

def tournament_selection( n_competitors ):
	competitors = np.random.permutation( list( range( population_size ) ) )
	tmp = [ data[i] for i in competitors[:n_competitors]]
	return min(tmp, key=lambda item: item["fit"])


def crossover( parent_1, parent_2):
	xt = list([ .5*( parent_1["xt"][i] + parent_2["xt"][i] ) for i in range(individual_size) ])
	devs = list([ math.sqrt( parent_1["dev"][i] + parent_2["dev"][i] ) for i in range(individual_size) ])
	fit = fitness_function( xt[0], xt[1] )
	return {"xt": xt, "dev": devs, "fit": fit}
	
def valid_individual( individual ):
	inLimit_1 = x_lower_limit <= individual["xt"][0] <= x_upper_limit
	inLimit_2 = x_lower_limit <= individual["xt"][1] <= x_upper_limit
	if inLimit_1  and  inLimit_2 :
		return True
	return False

def std_deviation(x, dev):
	return (math.exp(-0.5 * (x / dev) ** 2)) / (dev * math.sqrt(2 * math.pi))


def integral(lim_inf, lim_sup, dev, delta, rnd):
	area = 0.
	aux_sum = std_deviation(lim_inf, dev)
	aux = std_deviation(lim_inf, dev)

	lin_space = np.arange(lim_inf + delta, lim_sup, delta)
	for i in lin_space:
		aux_sum = std_deviation(i, dev)
		area += (aux + aux_sum)
		if (area * (delta / 2.) ) > rnd:
			return i
		aux = aux_sum
	return -1 * infinite

def mutation( individual ):
	for i in range( individual_size ):		
		individual["dev"][i] *= math.exp( integral(lim_inf, lim_sup, individual["dev"][i], delta, random.random() ))
		individual["xt"][i] += integral(lim_inf, lim_sup, individual["dev"][i], delta, random.random() )
	individual["fit"] = fitness_function( individual["xt"][0],individual["xt"][1])


def printBeautyData(individualsDataContainer):
	x=0
	for ind in individualsDataContainer:
		print "Individuo", x
		print "Xt : ",ind['xt']
		print "Stantard Deviation :",ind['dev']
		print "Fitness :",ind['fit']
		x+=1
		print "\n"


# u,lambda
def u_lambdaEE():
	global data
	iteration = 0
	lambda_size = int(population_size*1.5)

	generate_population( population_size )
	evaluate_population()

	while( iteration < n_iterations ):
		print "iteration #", iteration 

		for ms in range( lambda_size ):
			while( True ):
				parent_1=tournament_selection( n_competitors ) 
				parent_2=tournament_selection( n_competitors )
				new_individual = crossover( parent_1,parent_2)
				mutation(new_individual)
				if( valid_individual(new_individual) ):
					break
			data.append( new_individual )

		data = sorted( data, key=lambda x: x["fit"] )

		for ms in range( lambda_size ):
			del data[ len(data) -1 ]

		for i in range( population_size ):
			print data[i]["fit"]

		iteration+=1
	printBeautyData(data)

# u+lambda
def u_plus_lambdaEE():
	global data
	iteration = 0
	lambda_size = int(population_size*0.5)

	generate_population( population_size )
	evaluate_population()

	while( iteration < n_iterations ):
		print "iteration #", iteration 

		for ms in range( lambda_size ):
			while( True ):
				parent_1=tournament_selection( n_competitors ) 
				parent_2=tournament_selection( n_competitors )
				new_individual = crossover( parent_1,parent_2)
				mutation(new_individual)
				if( valid_individual(new_individual) ):
					break
			data.append( new_individual )

		data = sorted( data, key=lambda x: x["fit"] )

		for ms in range( lambda_size ):
			del data[ len(data) -1 ]

		for i in range( population_size ):
			print data[i]["fit"]

		iteration+=1
	printBeautyData(data)

# u+1
def u_1EE():
	global data
	iteration = 0
	generate_population( population_size )
	evaluate_population()
	
	while( iteration < n_iterations ):
		print "iteration #", iteration 

		while( True ):
			parent_1= tournament_selection( n_competitors )
			parent_2= tournament_selection( n_competitors )
			new_individual = crossover( parent_1,parent_2) 
			mutation(new_individual)
			
			if( valid_individual(new_individual) ):
				break

		data.append( new_individual )
		data = sorted( data, key=lambda x: x["fit"] )
		del data[ population_size ]

		iteration+=1

		for i in range( population_size ):
			print data[i]["fit"] 
	printBeautyData(data)
	


if __name__ == "__main__":
	#u_plus_lambdaEE()
	u_lambdaEE()
	#u_1EE()