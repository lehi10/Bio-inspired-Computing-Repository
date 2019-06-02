import random
import math
import numpy as np
import copy


distance_matrix = [ [0, 12, 3, 23, 1, 5, 23, 56, 12, 11],
				   [12, 0, 9, 18, 3, 41, 45, 5, 41, 27],
				   [3, 9, 0, 89, 56, 21, 12, 48, 14, 29],
				   [23, 18, 89, 0, 87, 46, 75, 17, 50, 42],
				   [1, 3, 56, 87, 0, 55, 22, 86, 14, 33],
				   [5, 41, 21, 46, 55, 0, 21, 76, 54, 81],
				   [23, 45, 12, 75, 22, 21, 0, 11, 57, 48],
				   [56, 5, 48, 17, 86, 76, 11, 0, 63, 24],
				   [12, 41, 14, 50, 14, 54, 57, 63, 0, 9],
				   [11, 27, 29, 42, 33, 81, 48, 24, 9, 0] ]


n_ants = 8
n_units = 10
initial_pheromones = 10

alpha = 1
beta = 1
p = 0.01
mp =0.2

n_iterations = 50
n_stagnant_iter = 20
initial_unit = random.randint( 0, n_units-1 )


best_global = {'path': [], 'cost': np.inf}

infinite = -1
dev = 0.1
delta = 0.1

pheromone_matrix = np.zeros(( n_units, n_units ))
visibility_matrix = np.zeros(( n_units, n_units ))

units = ['A', 'B', 'C', 'D', 'E', 'F', 'G','H','I','J']	

def print_matrix( matrix, text ):
	print( text )
	for i in range( n_units ):
		if(i==0):
			print("\tA\tB\tC\tD\tE\tF\tG" )
		for j in range( n_units ):
			if(j==0):
				print(units[i], end='\t')
			print( "{:.4f}".format(matrix[i][j]), end='\t')
		print()

def initialize_pheromone_matrix():
	for i in range( n_units ):
		for j in range( n_units ):
			if(i!=j):
				pheromone_matrix[i][j] = initial_pheromones

def initialize_visibility_matrix():
	tmp = distance_matrix 
	for i in range( len(tmp) ):
		for j in range( len(tmp) ):
			if i != j :
				if tmp[i][j] == 0 :
					visibility_matrix[i][j] = 10e-10
				else :
					visibility_matrix[i][j] = 1 / tmp[i][j]
			else :
				visibility_matrix[i][j]



def next_city( m_prob, random_number):
	probabilty_sum = 0
	for i in range( len(m_prob) ):
		if( m_prob[i] != -1 ):
			probabilty_sum += m_prob[i]
			if( random_number <= probabilty_sum ):
				return i

def std_deviation(x, dev):
	return (math.exp(-0.5 * (x / dev) ** 2))/(dev * math.sqrt(2 * math.pi))


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

def send_ants():
	path_list = []
	for i in range( n_ants ):
		path = []
		current_unit = initial_unit
		path.append( current_unit )
		print("Ant # ",i )
		print("Starting at: ", current_unit)
		while( len(path) < n_units ):
			m_sum = 0.
			sums_list = []


			for j in range( n_units ):
				if j not in path :
					t = (pheromone_matrix[current_unit][j]) ** alpha
					n = (visibility_matrix[current_unit][j]) ** beta
					tn = t*n
					sums_list.append( tn )
					m_sum += tn
					print( units[current_unit] + "-" + units[j], end=' ' )
					print( "t = ", t, end=' ' )
					print( "n = ", n, end=' ' )
					print( "t*n = ", tn )
				else:
					sums_list.append( -1 )
			print( "Sum: ", m_sum )
			m_prob = []
			for k in range( n_units ):
				if k not in path :
					m_prob.append( sums_list[k] / m_sum )
					print( units[current_unit] + "-" + units[k], end=' ' )
					print( "Probabilty = ", sums_list[k] / m_sum)
				else:
					m_prob.append(-1)
			random_number = random.random()
			print( "Random number: ", random_number )
			n_index = next_city( m_prob, random_number )
			print("Next city: ", units[n_index] )


			current_unit = n_index
			path.append( n_index )
		print("Ant # "+str(i)+": ", end='')
		for i in range( n_units ):
			if( i == n_units-1 ):
				print( units[path[i]])
			else:	
				print( units[path[i]] + "-", end='')
		path_list.append( path )
	return path_list

def path_cost( path ):
	m_sum = 0.
	for i in range( len( path )-1 ):
		m_sum += distance_matrix[path[i]][path[i+1]]
	return m_sum


def print_ant_results( path_list ):
	print("\nResults")
	costs_lists = []
	for j in range( len( path_list ) ):
		print("Ant # "+str(j)+": ", end='') 
		for i in range( n_units ):
			if( i == n_units-1 ):
				print( units[path_list[j][i]], end=' ')
			else:
				print( units[ path_list[j][i]] + "-", end='')
		costs_lists.append( path_cost(path_list[j]) ) 
		print( "Cost: ", costs_lists[j])
	index_ant = costs_lists.index( min(costs_lists) )
	worst_local = costs_lists.index( max(costs_lists) )
	print("------------------------------------------------------")
	print("Best Local Ant: ", end='')
	for i in range( n_units ):
		if( i == n_units-1 ):
			print( units[path_list[index_ant][i]], end=' ')
		else:
			print( units[path_list[index_ant][i]] + "-", end='')
	print("Cost: ", costs_lists[index_ant])
	print("------------------------------------------------------")

	if best_global['cost'] > costs_lists[index_ant] :
		best_global['path'] = list(path_list[index_ant])
		best_global['cost'] = costs_lists[index_ant]

	print("------------------------------------------------------")
	print("Best Global Ant: ", end='')
	for i in range( n_units ):
		if( i == n_units-1 ):
			print( units[best_global['path'][i]], end=' ')
		else:
			print( units[best_global['path'][i]] + "-", end='')
	print("Cost: ", best_global['cost'])
	print("------------------------------------------------------")

	return costs_lists, worst_local
	

def get_delta( i, j):
	for k in range( len(best_global['path']) -1 ):
		if ( best_global['path'][k] == i and best_global['path'][k+1] == j) or \
			( best_global['path'][k+1] == i and best_global['path'][k] == j):
			return 1 / best_global['cost']
	return 0

def arc_in_global( i, j):
	for k in range( len(best_global['path']) -1 ):
		if (i == best_global['path'][k] and j == best_global['path'][k+1]) or \
			( i == best_global['path'][k+1] and j == best_global['path'][k] ):
			return True
	return False

def second_evaporation( path, cost):
	print("Second evaporation:")
	for i in range( len(path) -1 ):
		if not arc_in_global( path[i], path[i+1] ) :
			print(units[path[i]]+" "+units[path[i+1]]+": Pheromone = ", end='')
			pheromone_matrix[path[i]][path[i+1]] =pheromone_matrix[path[i]][path[i+1]]*(1-p)
			print(pheromone_matrix[path[i]][path[i+1]])


def update_pheromone_matrix( path_list, costs_lists, worst_local ):

	for i in range( n_units ):
		for j in range( n_units ):
			tmp = 0
			if i != j :
				#print(units[i]+"-"+units[j]+": Pheromone = ", end='')
				delta = get_delta(i, j)
				#print( str(1-p)+"*"+str(pheromone_matrix[i][j])+"+"+str(delta)+" = ", end='')
				pheromone_matrix[i][j] = pheromone_matrix[i][j]*(1-p)+delta
				#print( pheromone_matrix[i][j] )

	#print("GLOBAL ", best_global['path'], " Cost:", best_global['cost'])
	#print("LOCAL", path_list[worst_local], " Cost:", costs_lists[worst_local])
	
	second_evaporation( path_list[worst_local], costs_lists[worst_local] )

	mean_threshold = 0
	for i in range( len( best_global['path'] ) -1 ):
		mean_threshold += pheromone_matrix[best_global['path'][i]][best_global['path'][i+1]]
		
	mean_threshold = mean_threshold / n_units
	
	#print("THRESHOLD ", mean_threshold)
	for i in range( n_units ):
		for j in range( n_units ):
			mut_random = random.random()
			if mp > mut_random :
				tmp = integral(-mean_threshold, mean_threshold, 0.00002, 0.01,random.random() )
				pheromone_matrix[i][j] += tmp 



def BWAS_algorithm():
	initialize_pheromone_matrix()
	initialize_visibility_matrix()
	global_counter = 0

	for i in range( n_iterations ):

		print("Iteration # ", i)
		if(i == 0):
			print_matrix( distance_matrix, " Distance Matrix " )
			print_matrix( pheromone_matrix, " Pheromone Matrix" )
			print_matrix( visibility_matrix, "Visibility Matrix" )

		path_list = send_ants()
		tmp = best_global['cost']
		cost_list, worst_local = print_ant_results( path_list )

		if( best_global['cost'] == tmp ):
			global_counter += 1
		else:
			global_counter = 0

		if n_stagnant_iter <= global_counter :
			initialize_pheromone_matrix()

		update_pheromone_matrix( path_list, cost_list ,worst_local )




if __name__ == "__main__":

	BWAS_algorithm()
