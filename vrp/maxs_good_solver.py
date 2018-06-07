#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
from collections import namedtuple
from gurobipy import *

Customer = namedtuple("Customer", ['index', 'demand', 'x', 'y'])

def length(customer1, customer2):
	return math.sqrt((customer1.x - customer2.x)**2 + (customer1.y - customer2.y)**2)

def solve_it(input_data):
	# Modify this code to run your optimization algorithm

	# parse the input
	lines = input_data.split('\n')

	parts = lines[0].split()
	customer_count = int(parts[0])
	vehicle_count = int(parts[1])
	vehicle_capacity = int(parts[2])
	
	customers = []
	for i in range(1, customer_count+1):
		line = lines[i]
		parts = line.split()
		customers.append(Customer(i-1, int(parts[0]), float(parts[1]), float(parts[2])))

	dist = {(i,j) :
		math.sqrt(sum((customers[i][k]-customers[j][k])**2 for k in [2,3]))
		for i in range(customer_count) for j in range(customer_count)}

	#the depot is always the first customer in the input
	depot = customers[0] 

	m = Model()

	# Create variables
	acts = {(c,v):
		m.addVar(vtype=GRB.BINARY, name='a_%d_%d'%(c,v))
		for c in range(customer_count)
		for v in range(vehicle_count)
	}

	edges = {(c1,c2,v):
		m.addVar(vtype=GRB.BINARY, obj=dist[(c1,c2)], name='e_%d_%d_%d'%(c1,c2,v))
		for c1 in range(customer_count)
		for c2 in range(c1+1)
		for v in range(vehicle_count)
	}

	for c1,c2,v in edges.keys():
		edges[c2,c1,v] = edges[c1,c2,v] 

	for c in range(customer_count):
		for v in range(vehicle_count):
			edges[c,c,v].ub = 0
	
	# only one vehicle can visit each customer except for the depot
	#m.addConstr(quicksum(acts[0,v] for v in range(vehicle_count)) == vehicle_count)
	for c in range(1,customer_count):
		m.addConstr(quicksum(acts[c,v] for v in range(vehicle_count)) == 1)

	for v in range(vehicle_count):
		for c in range(customer_count):
			m.addConstr(acts[c,v] <= acts[0,v])
	#break vehicle symmettry
	for v in range(vehicle_count-1):
		m.addConstr(acts[0,v] >= acts[0,v+1])

	#break vehicle symmettry
	for c in range(1,min(vehicle_count,customer_count)):
		
		for v in range(c,vehicle_count):
			m.addConstr(acts[c,v]==0)

	# unactivated customers can't have edges selected
	for c1 in range(customer_count):
		for c2 in range(c1):
			for v in range(vehicle_count):
				m.addConstr(edges[c1,c2,v] <= acts[c1,v])
				m.addConstr(edges[c1,c2,v] <= acts[c2,v])
	
	for v in range(vehicle_count):
		m.addConstr(quicksum(edges[0,c2,v] 
			for c2 in range(customer_count)
			) == 2*acts[0,v])
	for c1 in range(1,customer_count):
		m.addConstr(quicksum(edges[c1,c2,v] 
			for c2 in range(customer_count) 
			for v in range(vehicle_count)
			) == 2)
	
	for v in range(vehicle_count):
		m.addConstr(quicksum(acts[c,v] * customers[c].demand for c in range(customer_count)) <= vehicle_capacity)

	def subtourelim(model, where):
		if where == GRB.callback.MIPSOL:
			# make a list of edges selected in the solution
			for v in range(vehicle_count):
				selected = []
				for c1 in range(customer_count):
					sol = model.cbGetSolution([model._edges[c1,c2,v] for c2 in range(customer_count)])
					selected += [(c1,c2) for c2 in range(customer_count) if sol[c2] > 0.5]
				# find the shortest cycle in the selected edge list
				tour = subtour(selected,customer_count)
				if 2*len(tour) < len(selected):
				  # add a subtour elimination constraint
					expr = 0
					for c1 in range(len(tour)):
						for c2 in range(c1+1, len(tour)):
							expr += model._edges[tour[c1], tour[c2], v]
					#print("expr",expr)
					model.cbLazy(expr <= len(tour)-1)


	def subtour(edges,customer_count):
		if len(edges)==0:
			return([])
		#print(edges)
		n = customer_count
		visited = [False] * n
		cycles = []
		lengths = []
		selected = [[] for i in range(n)]
		for (x, y) in edges:
			selected[x].append(y)
		while True:
			current = visited.index(False)
			thiscycle = [current]
			while True:
				visited[current] = True
				neighbors = [x for x in selected[current] if not visited[x]]
				if len(neighbors) == 0:
					break
				current = neighbors[0]
				thiscycle.append(current)
			#cycles.append(thiscycle)
			#lengths.append(len(thiscycle))
			if len(thiscycle)>1:
				lengths.append(len(thiscycle))
				cycles.append(thiscycle)
				break
			if sum(lengths) == n:
				break
		#print("cycles",cycles)
		#print("cycles",cycles[lengths.index(min(lengths))])
		return cycles[lengths.index(min(lengths))]



			
	 
	m._acts = acts	
	m._edges = edges

	m.setParam('TimeLimit', 60.0)

	m.Params.lazyConstraints = 1
	m.optimize(subtourelim)

	# prepare the solution in the specified output format
	outputData = '%.2f' % m.objVal + ' ' + str(0) + '\n'
	for v in range(vehicle_count):
		selected = []
		for c1 in range(customer_count):
			sol = [edges[c1,c2,v].x for c2 in range(customer_count)]
			selected += [(c1,c2) for c2 in range(customer_count) if sol[c2] > 0.5]
		# find the shortest cycle in the selected edge list
		#print("sel: ",selected)
		if selected != []:
			tour = subtour(selected,customer_count)
			#print("tour: ",tour)
			#outputData += str(depot.index) + ' ' + ' '.join([str(customer) for customer in tour]) + ' ' + str(depot.index) + '\n'
			outputData += ' '.join([str(customer) for customer in tour]) + ' ' + str(depot.index) + '\n'

	return outputData


import sys

if __name__ == '__main__':
	import sys
	if len(sys.argv) > 1:
		file_location = sys.argv[1].strip()
		with open(file_location, 'r') as input_data_file:
			input_data = input_data_file.read()
		print(solve_it(input_data))
	else:

		print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/vrp_5_4_1)')

