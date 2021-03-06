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
    def search(i, color, domains, neighbors, unused_colors):
        global solution
        domains[i] = [color]
        if not prop_neighbors(i, domains, neighbors):     
            return False

        remaining_nodes = list(filter(lambda j: len(domains[j]) > 1, range(len(domains))))
        if len(remaining_nodes) == 0:
            solution = domains
            return True
        next_i = min(remaining_nodes, key=lambda j: (len(domains[j]) - 0.1 * len(neighbors[j])))

        for color_option in domains[next_i]:  
            if not color_option in unused_colors:
                if search(next_i, color_option, deepcopy(domains), neighbors, unused_colors):
                    return True
            else:
                unused_colors_copy = copy(unused_colors) 
                unused_colors_copy.remove(color_option)
                if search(next_i, color_option, deepcopy(domains), neighbors, unused_colors_copy):
                    return True
                return False
        
        '''
        for color_option in domains[next_i]:  
            if color_option in unused_colors:
                unused_colors_copy = copy(unused_colors) 
                unused_colors_copy.remove(color_option)
                if search(next_i, color_option, deepcopy(domains), neighbors, unused_colors_copy):
                    return True
                return False
            else:
                if search(next_i, color_option, deepcopy(domains), neighbors, unused_colors):
                    return True
        '''



    def prop_neighbors(i, domains, neighbors):
        q = queue.Queue()
        q.put(i)
        while not q.empty():
            i = q.get()
            color = domains[i][0]
            for neighbor in neighbors[i]:
                if color in domains[neighbor]:
                    domains[neighbor].remove(color)
                    if len(domains[neighbor]) == 0:
                        return False
                    if len(domains[neighbor]) == 1:
                        q.put(neighbor)

        return True


    def prop_neighbors2(i, nodes):
        color = nodes[i].domain[0]
        for neighbor in nodes[i].neighbors:
            if color in nodes[neighbor].domain:
                nodes[neighbor].domain.remove(color)
                if len(nodes[neighbor].domain) == 0:
                    print("halt")

                    return False
                if len(nodes[neighbor].domain) == 1:
                    prop_neighbors2(neighbor, nodes)
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

    domains = []
    neighbors = []
        
    foundSolution = False
    n_colors = 0
    while not foundSolution:
        n_colors += 1

        if n_colors > node_count:
            print("exiting, more colors  ({}) than nodes ".format(n_colors))
            break
        
        print("Trying {} colors".format(n_colors))
        domains = [copy(list(range(n_colors))) for _ in range(node_count)]
        neighbors = [copy([]) for _ in range(node_count)]
        for edge in edges:
            start, end = edge
            neighbors[start].append(end)
            neighbors[end].append(start)



        foundSolution = search(0,0,domains, neighbors,list(range(1,n_colors)))
        
        print(solution)
        
    

    # prepare the solution in the specified output format
    output_data = str(n_colors) + ' ' + str(1) + '\n'
    output_data += ' '.join(map(lambda domain: str(domain[0]), domains))

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

