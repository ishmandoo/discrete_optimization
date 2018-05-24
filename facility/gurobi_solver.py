#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple
import math
from gurobipy import *


Point = namedtuple("Point", ['x', 'y'])
Facility = namedtuple("Facility", ['index', 'setup_cost', 'capacity', 'location'])
Customer = namedtuple("Customer", ['index', 'demand', 'location'])

def length(point1, point2):
    return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)

def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    parts = lines[0].split()
    facility_count = int(parts[0])
    customer_count = int(parts[1])
    
    facilities = []
    for i in range(1, facility_count+1):
        parts = lines[i].split()
        facilities.append(Facility(i-1, float(parts[0]), int(parts[1]), Point(float(parts[2]), float(parts[3])) ))

    customers = []
    for i in range(facility_count+1, facility_count+1+customer_count):
        parts = lines[i].split()
        customers.append(Customer(i-1-facility_count, int(parts[0]), Point(float(parts[1]), float(parts[2]))))

    m = Model("mip1")

    facility_vars = [m.addVar(vtype=GRB.BINARY, name="fac_%d"%i) for i in range(facility_count)]
    edge_vars = [[m.addVar(vtype=GRB.BINARY, name="edge_%d_%d"%(i, j)) for j in range(facility_count)] for i in range(customer_count)]
    
    obj_fn = 0
    obj_fn += sum([facility.setup_cost * facility_var for facility, facility_var in zip(facilities, facility_vars)])
    obj_fn += sum([length(customers[i].location, facilities[j].location) * edge_vars[i][j] for j in range(facility_count) for i in range(customer_count)])
    
    # Set objective
    m.setObjective(obj_fn, GRB.MINIMIZE)

    # Add constraint: 

    [m.addConstr(sum([edge_vars[i][j] for j in range(facility_count)]) == 1) for i in range(customer_count)]

    [m.addConstr(sum([edge_vars[i][j]*customers[i].demand for i in range(customer_count)]) <= facilities[j].capacity*facility_vars[j]) for j in range(facility_count)]

    # Add constraint: x + y >= 1
    #m.addConstr(x + y >= 1, "c1")

    m.optimize()
    solution = []

    used = [0]*len(facilities)
    for facility_index in solution:
        used[facility_index] = 1

    for i in range(customer_count):
        for j in range(facility_count):
            if edge_vars[i][j].x == 1:
                solution.append(j)


    # prepare the solution in the specified output format
    output_data = '%.2f' % m.objVal + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, solution))

    return output_data


import sys

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/fl_16_2)')

