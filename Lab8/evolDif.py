import math
import random
import numpy as np


x_lower_limit = -1
x_upper_limit = 2

individual_size = 2 #or dimention

pop_size = 150
F = 0.5
CR = 0.9
n_iterations = 100

data = list()

def fitness_function(x,y):
	return x*math.sin(4*math.pi*x)-y*math.sin(4*math.pi*y+math.pi)+1


def generate_individual( size, min_limit, max_limit ):
	crom = [ random.uniform(min_limit, max_limit) for i in range(size)]
	fit = np.inf
	individual = {"crom":crom ,"fit":fit }
	return individual

def generate_population( population_size ):
	for i in range( population_size ):
		data.append( generate_individual( individual_size, x_lower_limit, x_upper_limit) )


def evaluate_population():
	for ind in data:
		ind["fit"] = fitness_function( ind["crom"][0], ind["crom"][1] )

def selection_ind(n_ind ):
	individuals = np.random.permutation(list(range(pop_size)))[:3]
	return individuals

def mutation(ind_1,ind_2,ind_3, target):
	t_ind_1 = np.array(data[ind_1]['crom'])
	t_ind_2 = np.array(data[ind_2]['crom'])
	t_ind_3 = np.array(data[ind_3]['crom'])
	v = t_ind_3 + F*(t_ind_1-t_ind_2)
	return v.tolist()

def crossover(difference_v,target):
	trial = [0]*individual_size
	for i in range(individual_size):
		nj=random.uniform(0,1)
		if nj < CR :
			trial[i]=difference_v[i]
		else:
			trial[i]=target[i]
	return trial
		

def printBeautyData(individualsDataContainer):
	x=0
	for ind in individualsDataContainer:
		print "Individuo", x
		print "\tcromosome : ",ind['crom']
		print "\tFitness :",ind['fit']
		x+=1


def onLimit(lower_limit,upper_limit,ind):
	if lower_limit<=ind[0]<upper_limit and lower_limit<=ind[1]<upper_limit:
		return 1
	return 0



def differentialEvolution():
	global data
	iteration = 0
	generate_population( pop_size )
	evaluate_population()
	
	print "Poblacion inicial :"
	printBeautyData(data)
	
	while( iteration < n_iterations ):
		print "iteration #", iteration 
		
		for i in range(pop_size):
			i_individuals= selection_ind( 3 )
			ind_1=i_individuals[0]
			ind_2=i_individuals[1]
			ind_3=i_individuals[2]
			mutated_ind= mutation(ind_1,ind_2,ind_3,i)
			print "Targer vector",data[i]['crom']
			print "\tMutated individual",mutated_ind
			trial = crossover(mutated_ind,data[i]['crom'])
			print "\tCrossed individual",trial
			
			
			
			fit = fitness_function(trial[0],trial[1])
			if onLimit(x_lower_limit,x_upper_limit,trial) and fit > data[i]['fit']: 	
				data[i]['crom']=trial
				data[i]['fit']=fit
				print "\tNew individual" , trial
				
		iteration+=1
	print "Poblacion final :"
	printBeautyData(data)
	
if __name__ == "__main__":
	differentialEvolution()
