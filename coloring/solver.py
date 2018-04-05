#!/usr/bin/python
# -*- coding: utf-8 -*-
from copy import copy

class Node():
    def __init__(self, index, domain):
        self.index = index
        self.domain = domain
        self.neighbors = []

    def __repr__(self):
        return "index: {}, neighbors: {}, domain: {}\n".format(self.index,self.neighbors,self.domain)
solution = None
def solve_it(input_data):
    global solution
    def search(i, color, nodes):
        global solution
        node = nodes[i]
        node.domain = [color]
        for neighbor in node.neighbors:
            if nodes[neighbor].domain == node.domain:
                return False
        if i == len(nodes)-1:
            solution = nodes
            #print("solution found: {}".format(solution))
            return True
        for color_option in nodes[i+1].domain:
            if search(i+1, color_option, copy(nodes)):
                return True

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
        
    foundSolution = False
    n_colors = 1
    while not foundSolution:
        print("Trying {} colors".format(n_colors))
        nodes = [Node(i,range(n_colors)) for i in range(node_count)]
        for edge in edges:
            start, end = edge
            nodes[start].neighbors.append(end)
            nodes[end].neighbors.append(start)
        sorted_nodes = sorted(nodes, key = lambda node:-len(node.neighbors))


        foundSolution = search(0,0,nodes)
        n_colors += 1

        if n_colors >= node_count:
            print(n_colors)
            break
        print(solution)
    

    # prepare the solution in the specified output format
    output_data = str(n_colors-1) + ' ' + str(1) + '\n'
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

