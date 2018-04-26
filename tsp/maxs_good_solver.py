#!/usr/bin/python
# -*- coding: utf-8 -*-
from random import randint, random
import math
from collections import namedtuple
import numpy as np
import matplotlib.pyplot as plt
from copy import copy

Point = namedtuple("Point", ['x', 'y'])

def length(point1, point2):
    return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)

def total_length(points, nodeCount, solution):
    obj = length(points[solution[-1]], points[solution[0]])
    for index in range(0, nodeCount-1):
        obj += length(points[solution[index]], points[solution[index+1]])
    return obj

def draw_solution(points, nodeCount, solution, solution_old):
    orderedXY = np.array([[points[i].x,points[i].y] for i in solution])
    #orderedXY = np.append(orderedXY,orderedXY[0])
    plt.plot(orderedXY[:,0],orderedXY[:,1],'ro-')
    orderedXY = np.array([[points[i].x,points[i].y] for i in solution_old])
    #orderedXY = np.append(orderedXY,orderedXY[0])
    plt.plot(orderedXY[:,0],orderedXY[:,1],'bo-')
    

def find_greedy(points, nodeCount):
    solution = [0]
    current_node = 0
    point_used = [False] * nodeCount
    point_used[0] = True 
    for i in range(nodeCount-1):
        closest_dist = 100000000000000
        for j, point in enumerate(points):
            if i != j:
                if not point_used[j] and length(point, points[current_node]) < closest_dist :
                    closest_dist = length(point, points[current_node])
                    best_node = j
        solution.append(best_node) 
        point_used[best_node] = True
        current_node = best_node
    return solution

def swap(solution, heads):
    head_a, head_b = heads
    solution[head_a:head_b] = reversed(solution[head_a:head_b])
    return solution

def random_heads(nodeCount):
    a = randint(0, nodeCount-1)
    b = randint(0, nodeCount-1)
    if abs(a - b) <= 1:
        return random_heads(nodeCount)
    return (min(a,b), max(a,b))

def boltzmann_factor(solution, points, nodeCount, heads, temp):
    head_a, head_b = heads
    point_head_a = points[solution[head_a]]
    point_head_b = points[solution[head_b]]
    point_tail_a = points[solution[head_a-1]]
    point_tail_b = points[solution[head_b-1]]

    current_length = length(point_head_a, point_tail_a) + length(point_head_b, point_tail_b)
    new_length = length(point_head_a, point_head_b) + length(point_tail_a, point_tail_b)
    delta_energy = new_length - current_length
    #print("\t dE = {}".format(delta_energy))
    factor = math.exp(-delta_energy / temp)
    return factor

def metropolis(solution, points, nodeCount, temp):
    heads = random_heads(nodeCount)
    factor = boltzmann_factor(solution, points, nodeCount, heads, temp)
    #print(factor)
    if factor > 1 or random() < factor:
        #rint("picked")
        #print(heads)
        #print("befo: {}".format(solution))
        #print(total_length(points, nodeCount, solution))
        solution = swap(solution, heads)
        #print("after: {}".format(solution))
        #print(total_length(points, nodeCount, solution))
    #print("length: {}".format(total_length(points, nodeCount, solution)))
    return solution

def solve_it(input_data):
    assert(swap([1,2,3,4,5,6,7],(3,5)) == [1,2,3,5,4,6,7])

    # parse the input
    lines = input_data.split('\n')

    nodeCount = int(lines[0])

    points = []
    for i in range(1, nodeCount+1):
        line = lines[i]
        parts = line.split()
        points.append(Point(float(parts[0]), float(parts[1])))

    # build a greedy solution
    # visit the nodes in the order they appear in the file
    solution = find_greedy(points, nodeCount)
    #solution = list(range(0, nodeCount))
    oldsol = copy(solution)
    bestYet = 1000000000
    bestSol = copy(solution)

    temp = 1.
    for _ in range(900000):
        
        solution = metropolis(solution, points, nodeCount, temp)
        #print(total_length(points, nodeCount, solution))
        obj = total_length(points, nodeCount, solution)
        if obj < bestYet:
            bestYet = obj
            bestSol = copy(solution)


    # calculate the length of the tour
    obj = total_length(points, nodeCount, solution)
    draw_solution(points, nodeCount, solution, solution)
    plt.show()

    if obj > bestYet:
        obj = bestYet
        solution = copy(bestSol)

    # prepare the solution in the specified output format
    output_data = '%.2f' % obj + ' ' + str(0) + '\n'
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
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/tsp_51_1)')

