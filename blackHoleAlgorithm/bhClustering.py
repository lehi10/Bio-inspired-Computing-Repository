import numpy as np
import random
import math

#cluster Parameters
numClusters 	= 3

#dataset parameters
originalDataSet = np.genfromtxt('tiny.data', delimiter=',' ,dtype="float")
dataSize = len(originalDataSet)
dimentionData 	= 2

dataSet=originalDataSet




#Algoritm Parameters
dimention 		= numClusters*dimentionData
populationSize 	= 3
numIterations 	= 10
lowerLimit 		= -100
upperLimit 		= 100

population=[]
blackHole={"star":[],"fitness":99999999}

clusterTags=[]


def printPopulation():
	for i in population:
		print i



def assigCluster():


	

def initPopulation():
	
	for i in range(populationSize):
	
		randCentroids=random.sample(range(0,dataSize), numClusters) 
		star=[]
		
		for k in range(numClusters):
			star+= dataSet[randCentroids[k]][1:].tolist()
			
		individual = {"star":star,"fitness":0}
		population.append(individual)
		
	
			
"""
def objetiveFunction(X):
	return X[0]**2+X[1]**2
	#return X[0]*math.sin(4*math.pi*X[0])-X[1]*math.sin(4*math.pi*X[1]+math.pi)+1
"""


def getAssociationWeight(i,j):
	if dataSet[i][0] == j+1:
		return 1
	else:
		return 0
	

def objetiveFunction(Z):
	res=0	
	for i in range(dataSize):
		for j in range(numClusters):		
			w = getAssociationWeight(i,j)
			Oi = dataSet[i][1:]
			Zj = Z[j*dimentionData:j*dimentionData+dimentionData]
			distance= np.linalg.norm(Oi-Zj)
			res+=(w*pow(distance,2))
	return res
	
	

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
	initPopulation()
	evaluatePopulation()
	for i in range(numIterations):
		evaluatePopulation()
		selectBlackHole()
		changeLocationsStars()
		findStartWithLowerCost()
		crossingEventHorizon()

		
initPopulation()
printPopulation()
evaluatePopulation()


				
#blackHoleAlgorithm()

#print "blackHole",blackHole


