import numpy as np
import random
import math

populationSize =3

dimention = 2
numIterations = 100

lowerLimit = -6
upperLimit = 2


population=[]

blackHole={"star":[],"fitness":99999999}

def printPopulation():
	for i in population:
		print i

def initPopulation():
	for i in range(populationSize):
		star =np.zeros(dimention)
		for j in range(dimention):
			star[j]=random.uniform(lowerLimit,upperLimit)
		individual = {"star":star,"fitness":0}
		population.append(individual)
			

def objetiveFunction(X):
	#return X[0]**2+X[1]**2
	return math.sin(X[0])+math.cos(X[1])+2

def evaluatePopulation():
	for individual in population:
		individual["fitness"]=objetiveFunction(individual["star"])

def selectBlackHole():
	global blackHole
	population.sort(key=lambda x: x["fitness"])
	if population[0]["fitness"]<blackHole["fitness"]:	
		blackHole=population.pop(0)
		
		star =np.zeros(dimention)
		for j in range(dimention):
			star[j]=random.uniform(lowerLimit,upperLimit)
		individual = {"star":star,"fitness":0}
		population.append(individual)
		
		
def changeLocationsStars():
	for individual in population:
		rand=np.random.rand(dimention)
		individual["star"]=individual["star"]+(rand*(blackHole["star"]-individual["star"]))
	evaluatePopulation()

def findStartWithLowerCost():
	global blackHole
	population.sort(key=lambda x: x["fitness"])

	if population[0]["fitness"] < blackHole["fitness"]:
		temp = population[0]
		population[0]=blackHole
		blackHole=temp



def crossingEventHorizon():
	sumFi=sum([ i['fitness'] for i in population])	
	R=blackHole["fitness"]/(sumFi)

	for inv in population:
		euclideanDistance=np.linalg.norm(blackHole["star"]-inv["star"]) 
		if euclideanDistance <  R:
			star =np.zeros(dimention)
			for j in range(dimention):
				star[j]=random.randint(lowerLimit,upperLimit)
			inv["star"]=star
			


def blackHoleAlgorithm():
	print "Inicializando poblacion"
	initPopulation()
	printPopulation()
	evaluatePopulation()
	for i in range(numIterations):
		evaluatePopulation()

		selectBlackHole()
		changeLocationsStars()
		findStartWithLowerCost()
		crossingEventHorizon()
		print blackHole

				
blackHoleAlgorithm()

print ""
print ""
print ""
print "blackHole",blackHole

print ""
print ""
print ""
