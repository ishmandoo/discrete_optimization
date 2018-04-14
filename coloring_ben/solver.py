#!/usr/bin/python
# -*- coding: utf-8 -*-
from copy import deepcopy, copy
import queue

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
    global sorted_nodes
    def search(i, color, nodes):
        global solution
        global sorted_nodes

        #sorted_i = sorted_nodes[i].index
        node = nodes[i]
        node.domain = [color]
        if not prop_neighbors(i, nodes):     
            return False

        for neighbor in node.neighbors:
            if nodes[neighbor].domain == node.domain:
                print("No fucking way this should run")
                return False
        remaining_nodes = list(filter(lambda node: len(node.domain) > 1, nodes))
        if len(remaining_nodes) == 0:
            solution = nodes
            return True
        next_node = min(remaining_nodes, key=lambda node: (len(node.domain) - 0.1 * len(node.neighbors)))
        next_i = next_node.index
        for color_option in nodes[next_i].domain:    
            if search(next_i, color_option, deepcopy(nodes)):
                return True

    def prop_neighbors(i, nodes):
        q = queue.Queue()
        q.put(i)
        while not q.empty():
            i = q.get()
            color = nodes[i].domain[0]
            for neighbor in nodes[i].neighbors:
                if color in nodes[neighbor].domain:
                    nodes[neighbor].domain.remove(color)
                    if len(nodes[neighbor].domain) == 0:
                        return False
                    if len(nodes[neighbor].domain) == 1:
                        q.put(neighbor)

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
    n_colors = 0
    while not foundSolution:
        n_colors += 1

        if n_colors > node_count:
            print("exiting, more colors  ({}) than nodes ".format(n_colors))
            break
        
        print("Trying {} colors".format(n_colors))
        nodes = [Node(i,list(range(n_colors))) for i in range(node_count)]
        for edge in edges:
            start, end = edge
            nodes[start].neighbors.append(end)
            nodes[end].neighbors.append(start)
        sorted_nodes = sorted(nodes, key = lambda node:-len(node.neighbors))

        foundSolution = search(sorted_nodes[0].index,0,nodes)
        
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

