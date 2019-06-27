import math
import random
import numpy as np
#Parameters

lowerLimit = -10
upperLimit = 10

populationSize = 4
selectionSize=4
randomCells=2
cloneRate = 0.25
mutationFactor = -2.5
numOfBits = 8



numOfIterations = 100
	
population = []


def printPopulation():
	for i in range(selectionSize):
		print population[i]

def generateBitsStr():
	bitStr = np.random.randint(2, size=numOfBits*2)
	str1 = ''.join(str(e) for e in bitStr)
	vec1=int(str1[:8],2)
	vec2=int(str1[8:],2)
	return str1, vec1,vec2
	
def costFunction(vec):
	return - math.cos(vec[0])*math.cos(vec[1])*math.exp(-(vec[0]-math.pi)**2-(vec[1]-math.pi)**2)

def normalize(X):
	return lowerLimit+((upperLimit-lowerLimit)/(2.0**8-1.0))*X


def getAffinity(cost):
	return 1.0-(cost/(upperLimit-lowerLimit))

def getMutationRate(affinity):
	return math.exp(mutationFactor*affinity)

def getNumClones():
	return populationSize*cloneRate

def initPopulation():
	for i in range(populationSize):	
		bitsStr,vec1,vec2=generateBitsStr()
		vector=[normalize(vec1),normalize(vec2)]
		cost = costFunction(vector)
		individual = {'bitsStr':bitsStr,'vector':vector ,'cost':cost,'affinity':0}
		population.append(individual)



def evaluePopulationAffinity():
	for i in range(populationSize):	
		population[i]['affinity']=getAffinity(population[i]['cost'])
	
	
def select():
	global population
	population.sort(key=lambda x: x['cost'])
	population=population[:selectionSize]


def getIndividualCloned(strBits):
	vec1=int(strBits[:8],2)
	vec2=int(strBits[8:],2)
	vector=[normalize(vec1),normalize(vec2)]
	cost = costFunction(vector)
	individual = {'bitsStr':strBits,'vector':vector ,'cost':cost,'affinity':0}
	return individual



def clonalg():
	initPopulation()
	for i in range(numOfIterations):
		evaluePopulationAffinity()
		#selection
		select()
		for j in range(populationSize):
			#num of clones
			print "Numero de clones : ", int(getNumClones())
			for k in range(int(getNumClones())):				
				mutationRate=getMutationRate(population[j]['affinity'])
				clone= list(population[j]['bitsStr'])
				
				# make mutation
				for it in range(numOfBits*2):
					rnd=random.uniform(0,1)
					if rnd < mutationRate : 
						clone[it]=str((int(population[j]['bitsStr'][it])+1)%2)
				clone="".join(clone)		
				newClone=getIndividualCloned(clone)
				print "Nuevo Clon"
				print newClone
				population.append(newClone)
		#Selection
		select()		
		for i in range(2):
			bitStr = np.random.randint(2, size=numOfBits*2)
			str1 = ''.join(str(e) for e in bitStr)
			clone=str1
			newClone=getIndividualCloned(clone)
			population.append(newClone)
		select()
		print "\nPopulation:"
		printPopulation()
		
clonalg()


print "\nResultado Final\n",
print population[0]		

	
	
	
	
	
	
	
	
