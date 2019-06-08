import math
import random
import numpy as np
#Parameters

lowerLimit = -1
upperLimit = 2

CS 	= 6
NS 	= 10
D	= 2
L	= (CS*D)/2

numOfIterations = 200

	
population = []
bestSolVec = []

memory={'x1':0,'x2':0,'fx':0,'fit':0}


def printPopulation():
	for i in range(NS):
		print(population[i])
	

def objetiveFunction(x,y):
	return x*math.sin(4*math.pi*x)-y*math.sin(4*math.pi*y+math.pi)+1

def checkLimits(x):
	if lowerLimit<x and x<upperLimit:
		return True
	return False
	
def newParticle(x1,x2):
	individual = {'x1': x1,'x2':x2 ,'fx':0 ,'fit':0 , 'cont':0}
	return individual

def calculeFitness(fx):
	if fx >=0:
		return 1.0/(1+fx)
	else:
		return 1+abs(fx)

	
def initialPopulation():
	global population
	
	for i in range(NS):
		x1=random.uniform(lowerLimit,upperLimit)
		x2=random.uniform(lowerLimit,upperLimit)

		population.append(newParticle(x1,x2))
		
	for i in range(NS):
		temp = {'x1':0,'x2':0,'fx':0,'fit':0,'p':0,'piacum':0,'cont':0}
		bestSolVec.append(temp)


def evaluatePopulation():
	global population
	for i in range(NS):
		x1=population[i]['x1']
		x2=population[i]['x2']
		
		fx=objetiveFunction(x1,x2)		
		fit=calculeFitness(fx)
		
		population[i]['fx']= fx
		population[i]['fit']= fit
		population[i]['count']= 0

def getRandDiffOf(lowerV,upperV,x):		
	res=x
	while res == x:
		res = random.randint(lowerV,upperV)
	return res
	
		
def newSolutionVectors():
	vecOfSol=[]
	for i in range(NS):
	
		k=getRandDiffOf(0,NS-1,i)
		j=random.randint(0,1)
		o=random.uniform(-1,1)
		
		
		v=[population[i]['x1'],population[i]['x2']]
		
		if j == 0 :		
			tempSol=population[i]['x1']+o*(population[i]['x1']-population[k]['x1'])
			while checkLimits(tempSol)==False:
				o=random.uniform(-1,1)
				tempSol=population[i]['x1']+o*(population[i]['x1']-population[k]['x1'])
			v[j]=tempSol
			
		if j == 1 :
			tempSol = population[i]['x2']+o*(population[i]['x2']-population[k]['x2'])
			while checkLimits(tempSol)==False:
				o=random.uniform(-1,1)
				tempSol=population[i]['x2']+o*(population[i]['x2']-population[k]['x2'])
			v[j]=tempSol
			
		fx=objetiveFunction(v[0],v[1])
		fit = calculeFitness(fx)
		
		mejora = 0
		cont = population[i]['cont']
		
		if fit < population[i]['fit']:
			mejora = 1
			cont = 0
		else :
			cont+=1
		
		sol={'k':k,'j':j,'o':o,'v1':v[0],'v2':v[1],'fx':fx,'fit':fit,'mejora':mejora,'cont':cont}
		
		vecOfSol.append(sol)
		
	return vecOfSol
		
		

def getBestSol(vecOfSol):
	global bestSolVec
	for i in range(NS):
		if vecOfSol[i]['fit'] < population[i]['fit']:
			temp ={'x1':vecOfSol[i]['v1'],'x2':vecOfSol[i]['v2'],'fx':vecOfSol[i]['fx'],'fit':vecOfSol[i]['fit'],'p':0,'piacum':0,'cont':vecOfSol[i]['cont']}
			bestSolVec[i]=temp
			
		else :
			temp = {'x1':population[i]['x1'],'x2':population[i]['x2'],'fx':population[i]['fx'],'fit':population[i]['fit'],'p':0,'piacum':0,'cont':population[i]['cont']}
			bestSolVec[i]=temp

	
	
def calcProb():
	total = 0
	acc = 0
	for i in range(NS):
		total+=bestSolVec[i]['fit']
	for i in range(NS):
		bestSolVec[i]['p'] = bestSolVec[i]['fit'] / total
		bestSolVec[i]['pacum'] = acc + bestSolVec[i]['fit']
		acc += bestSolVec[i]['fit']

	
def getIndividualByProb(num):
	for i in range(NS):

		if num <= bestSolVec[i]['pacum']:
			return i
		
def observers():
	global bestSolVec
	for i in range(NS):
		rnd=random.uniform(0,1)
		itFuente=getIndividualByProb(rnd)
		
		k=getRandDiffOf(0,NS-1,itFuente)
		j=random.randint(0,1)
		
		o=random.uniform(-1,1)
		
		
		v=[bestSolVec[i]['x1'],bestSolVec[i]['x2']]
		
		if j == 0 :		
			tempSol=bestSolVec[itFuente]['x1']+o*(bestSolVec[itFuente]['x1']-bestSolVec[k]['x1'])
			while checkLimits(tempSol)==False:
				o=random.uniform(-1,1)
				tempSol=bestSolVec[itFuente]['x1']+o*(bestSolVec[itFuente]['x1']-bestSolVec[k]['x1'])
			v[j]=tempSol
			
		if j == 1 :
			tempSol=bestSolVec[itFuente]['x2']+o*(bestSolVec[itFuente]['x2']-bestSolVec[k]['x2'])
			while checkLimits(tempSol)==False:
				o=random.uniform(-1,1)
				tempSol=bestSolVec[itFuente]['x2']+o*(bestSolVec[itFuente]['x2']-bestSolVec[k]['x2'])
				v[j]=tempSol
		
		fx=objetiveFunction(v[0],v[1])
		fit = calculeFitness(fx)
		
		cont = bestSolVec[itFuente]['cont']
		if fit < bestSolVec[i]['fit']:
			mejora = 1
			cont = 0
			temp = {'x1':v[0],'x2':v[1],'fx':fx,'fit':fit,'p':0,'piacum':0,'cont':cont}
			bestSolVec[itFuente]=temp
			
		else :
			cont+=1
			bestSolVec[itFuente]['cont']+=1
		
		calcProb()


def getMaxSolution():
	best=-1
	itBest=-1
	for i in range(NS):
		if bestSolVec[i]['fit'] <= best:
			itBest=i
			best=bestSolVec[i]['fit']
	return itBest 
		
def memorizeSolution():
	
	itBest=getMaxSolution()
	if bestSolVec[itBest]['fx']>memory['fx']:
		memory['x1']=bestSolVec[itBest]['x1']
		memory['x2']=bestSolVec[itBest]['x2']
		memory['fx']=bestSolVec[itBest]['fx']
		memory['fit']=bestSolVec[itBest]['fit']
		

def newSources():
	for i in range(NS):
		population[i]=bestSolVec[i]
	for i in range(NS):
		if population[i]['cont']>=L:
			rand1=(random.uniform(0,1))
			rand2=(random.uniform(0,1))
			
			x1=lowerLimit+rand1*(upperLimit-lowerLimit)
			x2=lowerLimit+rand2*(upperLimit-lowerLimit)
			population[i]['x1']=x1
			population[i]['x2']=x2
	
	

def psoAlgorithm():
	initialPopulation()
	print ("Population :")
	evaluatePopulation()
	printPopulation()
	print("----------------------------------")
	for i in range(numOfIterations):
		vecOfSol=newSolutionVectors()
		getBestSol(vecOfSol)
		calcProb()
		observers()
		newSources()
		evaluatePopulation()
		memorizeSolution()
	print "Best Solution",memory
		
		
		
				
psoAlgorithm()


	
	
	
	
	
	
	
	
