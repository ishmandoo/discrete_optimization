#!/usr/bin/python
# -*- coding: utf-8 -*-
from ortools.constraint_solver import pywrapcp


solution = None
def solve_it(input_data):
    def search(n_colors, node_count, edges):

        solver = pywrapcp.Solver("coloring")

        # Creates the variables.
        # The array index is the column, and the value is the row.
        colors = [solver.IntVar(0, n_colors - 1, "x%i" % i) for i in range(node_count)]

        solver.Add(colors[0] == 0)
        for edge in edges:
            start, end = edge
            solver.Add(colors[start] != colors[end])

        db = solver.Phase(colors, solver.INT_VAR_SIMPLE, solver.ASSIGN_MIN_VALUE)

        solver.NewSearch(db)

        print("done")
        while solver.NextSolution():
            print("solution found", colors)
            return colors

        return None

    # parse the input
    lines = input_data.split('\n')

    first_line = lines[0].split()
    node_count = int(first_line[0])
    edge_count = int(first_line[1])

    edges = []
    for i in range(1, edge_count + 1):
        line = lines[i]
        parts = line.split()
        edges.append((int(parts[0]), int(parts[1])))
        
    n_colors = 0
    solution = None
    while solution is None:
        n_colors += 1

        if n_colors > node_count:
            print("exiting, more colors  ({}) than nodes ".format(n_colors))
            break
        
        print("Trying {} colors".format(n_colors))
        solution = search(n_colors, node_count, edges)
        
        print(solution)
        
    

    # prepare the solution in the specified output format
    output_data = str(n_colors) + ' ' + str(1) + '\n'
    output_data += ' '.join(map(lambda node: str(node.domain[0]), solution))

    return output_data


import sys

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        #solve_it(input_data)
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/gc_4_1)')

