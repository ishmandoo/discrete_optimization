#!/usr/bin/python
# -*- coding: utf-8 -*-
from gurobipy import *
from collections import namedtuple
Item = namedtuple("Item", ['index', 'value', 'weight','density','taken'])



best_result = 0

def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    firstLine = lines[0].split()
    item_count = int(firstLine[0])
    capacity = int(firstLine[1])
    m = Model("mip1")
    items = []
    gurobiVars = []
    for i in range(1, item_count+1):
        line = lines[i]
        parts = line.split()
        items.append(Item(i-1, int(parts[0]), int(parts[1]),float(parts[0])/float(parts[1]),0))
        gurobiVars.append(m.addVar(vtype=GRB.BINARY, name=str(i)))
    # a trivial greedy algorithm for filling the knapsack
    # it takes items in-order until the knapsack is full
    value = 0
    weight = 0
    taken = [0]*len(items)


    

    
    # Set objective
    m.setObjective(sum([item.value*gurobiVar for item,gurobiVar in zip(items,gurobiVars)]), GRB.MAXIMIZE)

    # Add constraint: x + 2 y + 3 z <= 4
    m.addConstr(sum([item.weight*gurobiVar for item,gurobiVar in zip(items,gurobiVars)]) <= capacity , "c0")

    m.optimize()

    # for v in m.getVars():
    #     print('%s %g' % (v.varName, v.x))

    print('Obj: %g' % m.objVal)

    



    # prepare the solution in the specified output format
    output_data = str(m.objVal) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(lambda var:str(int(var.x)), gurobiVars))
    return output_data


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)')






