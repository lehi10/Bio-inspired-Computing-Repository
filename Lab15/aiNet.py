import math
import random
import numpy as np
import scipy.stats as ss

from scipy.spatial import distance


#Parameters

lowerLimit = -10
upperLimit = 10

numOfIterations = 200
populationSize = 5
problem_size=2
n_clones = 5
n_rand = 2
affinity_threshold = 0.5
beta = 100


infinite = -1

population = []


def printPopulation():
	for i in range(populationSize):
		print(population[i])

def costFunction(vec):
	return - math.cos(vec[0])*math.cos(vec[1])*math.exp(-(vec[0]-math.pi)**2-(vec[1]-math.pi)**2)
	#return vec[0]**2+vec[1]**2

def evaluateVector():
	for i in range(populationSize):	
		cost = costFunction(population[i]['vector'])
		population[i]['cost']=cost
	
	
def normalize(individual,maxCost,minCost):
	return 1.0 - (individual['cost']/(maxCost-minCost))


def normalizeCosts():
	population.sort(key=lambda x: x['cost'])
	minCost=population[0]['cost']
	maxCost=population[populationSize-1	]['cost']
	
	for i in range(populationSize):
		population[i]['norm_cost']=normalize(population[i], maxCost,minCost)


def avgPopulation():
	avg=0
	for i in range(populationSize):
		avg+=population[i]['cost']
	return avg/populationSize


def initPopulation():
	for i in range(populationSize):	
		vector=[]
		for it_vec in range(problem_size):
			rand_value=random.uniform(lowerLimit,upperLimit)
			vector.append(rand_value)
		
		individual ={'vector':vector, 'cost':0,'norm_cost':0 }
		population.append(individual)


def std_deviation(x, dev):
	return (math.exp(-0.5 * (x / dev) ** 2))/(dev * math.sqrt(2 * math.pi))


def random_gaussian():
	mean=0.0
	stdev=1.0
	
	u1 = 0
	u2 = 0 
	w = 0
	while True:
		u1 = 2 * random.uniform(0,1) - 1.0
		u2 = 2 * random.uniform(0,1) - 1.0
		w = u1 * u1 + u2 * u2
		if w < 1:
			break
	
	w = math.sqrt((-2.0 * math.log(w)) / w)
	
	return mean + (u2 * w) * stdev
  
  




def createRandomCell():
	v1=random.uniform(lowerLimit,upperLimit)
	v2=random.uniform(lowerLimit,upperLimit)
	
	vector=[v1,v2]
	cost=costFunction(vector)
	
	individual ={'vector':vector, 'cost':cost,'norm_cost':0 }
	return individual 
	
	
def mutation_rate(beta, normalized_cost):
	return (1.0/beta) * math.exp(-normalized_cost)
  
  

def get_neighborhood(cell, pop, aff_thresh):
	neighbors = []
	for p in pop:
		if distance.euclidean(p['vector'],cell) < aff_thresh:
			neighbors.append(p)
	return neighbors


def affinity_supress(population_vec, aff_thresh):
	pop = []
	for cell in population_vec:	
		neighbors = get_neighborhood(cell['vector'], population, aff_thresh)
		neighbors.sort(key=lambda x: x['cost'])		
		if len(neighbors)==0 or cell == neighbors[0]:
			pop.append(cell)


	return pop



progeny=[]

def opt_aiNet():
	global population
	initPopulation()
	for it in range(numOfIterations):
		print "Iteracion ",it
		evaluateVector()
		progeny=[]
		normalizeCosts()
		avgCost = avgPopulation()
		
		print "Promedio Costos ",avgCost

		#while avgPopulation() > avgCost:
		for i in range(populationSize):
			clones=[]
			for itClone in range(n_clones):
				alpha = mutation_rate(beta, population[i]['norm_cost'])
				desvNorm = alpha*random_gaussian()

				v1=population[i]['vector'][0]+alpha*desvNorm
				v2=population[i]['vector'][1]+alpha*desvNorm
				
				vector=[v1,v2]
				cost=costFunction(vector)
				
				individual_C ={'vector':vector, 'cost':cost,'norm_cost':0 }
				clones.append(individual_C)
		
			print "\nClones "
			for itC in clones:
				print itC
			
			clones.sort(key=lambda x: x['cost'])
			progeny.append(clones[0])
		
		affinity_supress(progeny,affinity_threshold)
		
		
		for i in range(n_clones):
			progeny.append(createRandomCell())
		
		population=progeny
			

opt_aiNet()


print("\nResultado Final\n")

print population[0]

	
	
	
	
	
	
	
	
