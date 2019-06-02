import math
import random

#Parameters

lowerLimit = -1
upperLimit = 2

numOfParticles = 5
numOfIterations = 100

phi1 = 2.0
phi2 = 2.0

	
population = []
gBest = {'x1': 0,'x2':0 ,'fit':0}
lBest = []


def printPopulation():
	for i in range(numOfParticles):
		print population[i]
	

def objetiveFunction(x,y):
	return x*math.sin(4*math.pi*x)-y*math.sin(4*math.pi*y+math.pi)+1

def checkLimits(x):
	if lowerLimit<x and x<upperLimit:
		return True
	return False
	
def newParticle(x1,x2,v1,v2):
	individual = {'x1': x1,'x2':x2 , 'v1':v1,'v2':v2 ,'fit':0}
	return individual


	
def initialPopulation():
	global population
	
	for i in range(numOfParticles):
		x1=random.uniform(lowerLimit,upperLimit)
		x2=random.uniform(lowerLimit,upperLimit)
		v1=random.uniform(-1,1)
		v2=random.uniform(-1,1)
		population.append(newParticle(x1,x2,v1,v2))
		

def evaluateFitness():
	global population
	global gBest
	global lBest
	for i in range(numOfParticles):
		x1=population[i]['x1']
		x2=population[i]['x2']
		fitness=objetiveFunction(x1,x2)		
		population[i]['fit']= fitness
		#Inicializando Best Local
		lBest.append({'x1':x1,'x2':x2,'fit':fitness})
		


def getBestParticle():
	global lBest
	for i in range(numOfParticles):
		if particles[i]['fit'] > lBest[i]['fit']:
			lBest[i]['x1']=particles[i]['x1']
			lBest[i]['x2']=particles[i]['x2']
			lBest[i]['fit']=particles[i]['fit']
			print "Best Local Particle #",i,"  X1:", lBest[i]['x1'] ,'\tX2',lBest[i]['x2']
	
	
def obtainBestGlobal():
	global gBest
	bestGlobal=max(population, key=lambda x: x['fit'])
	if bestGlobal['fit'] > gBest['fit']: 		
		gBest['x1']=bestGlobal['x1']
		gBest['x2']=bestGlobal['x2']
		gBest['fit']=bestGlobal['fit']
		print "Best Global " ," X1:", gBest['x1'] ,'\tX2',gBest['x2']
		
	
def calculeParticleVelocity():
	global population
	w=random.uniform(0,1)
	for i in range(numOfParticles):
		x1=upperLimit+1
		x2=upperLimit+1
		v1 = 0
		v2 = 0
		while not checkLimits(x1) or not checkLimits(x2) :
			rand1=random.uniform(0,1)
			rand2=random.uniform(0,1)

			x1=population[i]['x1']
			x2=population[i]['x2']
			
			v1=w*population[i]['v1']+phi1*rand1*(lBest[i]['x1']-x1)+phi2*rand2*(gBest['x1']-x1)
			v2=w*population[i]['v2']+phi1*rand1*(lBest[i]['x2']-x2)+phi2*rand2*(gBest['x2']-x2)
			
			x1=x1+v1
			x2=x2+v2

		print "New Positions"
		print "X1:",x1,"\tX2:", x2
		print "New Velocities"
		print "V1:",v1,"\tV2:", v2
		print "-------------------------------"
		population[i]['v1']=v1
		population[i]['v2']=v2	
	
		population[i]['x1']=x1
		population[i]['x2']=x2
		
		
	return 0
		
def psoAlgorithm():
	initialPopulation()
	print "Population :"
	printPopulation()
	print "----------------------------------"
	for i in range(numOfIterations):
		evaluateFitness()
		obtainBestGlobal()
		calculeParticleVelocity()
		
psoAlgorithm()


print "Resultado : ",gBest

	

# 1.6
# 1.6
# 4
	
	
	
	
	
	
	
	
