import numpy as np
import random

tam=10

population=[]


def function_1(x,y):
	return 4*x**2+4*y**2
	
def function_2(x,y):
	return (x-5)**2+(y-5)**2
	
def generatePopulation(array):
	for i in array:
		i[0]=function_1(random.randint(0,5),random.randint(0,3))
		i[1]=function_2(random.randint(0,5),random.randint(0,3))
	print "Poblacion Inicial \n"
	print array
	print "\n"

def BLX(p_1, p_2):
	alpha=0.5
	beta=random.uniform(-1*alpha,1+alpha)
	c_1=p_1[0]+beta*(p_2[0]-p_1[0])
	c_2=p_1[1]+beta*(p_2[1]-p_1[1])
	print "Cruzamiento BLX "
	print "Padres ", p_1 , p_2 
	print "Hijo : ",[c_1,c_2]
	print "\n"
	return [[c_1,c_2]]

def identify_pareto(scores):
    population_size = scores.shape[0]
    population_ids = np.arange(population_size)
    pareto_front = np.ones(population_size, dtype=bool)
    for i in range(population_size):
        for j in range(population_size):
            if all(scores[j] <= scores[i]) and any(scores[j] < scores[i]):
                pareto_front[i] = 0
                break
    return population_ids[pareto_front]
    


def mutacion_uniforme(cromosoma):
	gen_i=random.randint(0,1)
	cromosoma[gen_i]=function_2(random.randint(0,5),random.randint(0,3))
	
def generateOffspring(array):	
	i=random.randint(0,9)
	j=random.randint(0,9)
	
	while i==j:
		i=random.randint(0,9)
		j=random.randint(0,9)
	
	son = BLX(array[i],array[j])
	return son
	
	
def last_pareto_selected(array, num_selected):
	selected=[]
	selected.append(array[0])
	if len(selected) < num_selected:
		selected.append(array[len(array)-1])	
	
	if len(selected) == num_selected:
		return selected
	
	posible_selected=[]
	for i in range(1,len(array)-1):
		crowdis=2*(abs(abs(array[i-1][0])-abs(array[i+1][0])) + abs(abs(array[i-1][1])-abs(array[i+1][1])))
		posible_selected.append([i,crowdis])

	posible_selected=sorted(posible_selected, reverse=True , key=lambda x: x[1])
	
	it=0
	while len(selected) < num_selected:
		selected.append(posible_selected[it])
		it=it+1
	
	return selected
	
	
def test():
	population= np.zeros((tam,2))
	generatePopulation(population)	
	pareto_front=[]

	
	for it_loop in range(0,100):
		for i in range(0,int(tam/2)):
			n_crom = generateOffspring(population)
			population=np.append(population, n_crom,axis=0)
	
		it_pareto = 0
		while len(population) > 0:
		
			array_pFront =identify_pareto(population)
			print "Frontera de Pareto # ", it_pareto
			print population[array_pFront]
			print "\n"
			front_i = np.zeros(shape=(0,2))
			for i in array_pFront:
				front_i=np.append(front_i,[population[i]],axis=0)
			pareto_front.append([])
			pareto_front[it_pareto]=front_i.tolist()
			array_pFront=np.sort(array_pFront)[::-1]
		
			for i in array_pFront:
				population=np.delete(population,i,0)
		
			it_pareto=it_pareto+1
		it_pareto=0
				
		while len(population) < tam:
			new_pareto_front=pareto_front[it_pareto]
			if len(new_pareto_front)+len(population) <= tam:
				for crom in new_pareto_front:		
					population=np.append(population,[crom],axis=0)
				it_pareto=it_pareto+1
			else:
				new_pareto_front=np.sort(new_pareto_front,axis=0)
				last_pareto=last_pareto_selected(new_pareto_front,tam-len(population))
				population=np.append(population,last_pareto,axis=0)
				return population

print "Poblacion Final :"
print test()


