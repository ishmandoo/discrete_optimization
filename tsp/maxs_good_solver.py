#!/usr/bin/python
# -*- coding: utf-8 -*-
from random import randint, random, shuffle
import math
from collections import namedtuple
import numpy as np
import matplotlib.pyplot as plt
from copy import copy

Point = namedtuple("Point", ['x', 'y'])
#lengths = None

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
    try: 
        factor = math.exp(-delta_energy / temp)
    except:
        factor = 0

    return factor, delta_energy

def find_temp_scale(solution, points):
    scale = [length(points[i],points[j]) for (i,j) in zip(solution[1:], solution[:-1])]
    return np.std(scale)

def metropolis(solution, points, nodeCount, temp):
    heads = random_heads(nodeCount)
    factor, delta_length = boltzmann_factor(solution, points, nodeCount, heads, temp)

    if factor > 1 or random() < factor:
        solution = swap(solution, heads)
    else:
        delta_length = 0

    return solution, delta_length

def solve_it(input_data):
    #global lengths
    assert(swap([1,2,3,4,5,6,7],(3,5)) == [1,2,3,5,4,6,7])

    # parse the input
    lines = input_data.split('\n')

    nodeCount = int(lines[0])

    points = []
    for i in range(1, nodeCount+1):
        line = lines[i]
        parts = line.split()
        points.append(Point(float(parts[0]), float(parts[1])))

    #lengths = np.array([[length(points[i], points[j]) for j in range(nodeCount)] for i in range(nodeCount)])

    # build a greedy solution
    # visit the nodes in the order they appear in the file
    #greedy_solution = find_greedy(points, nodeCount)
    greedy_solution = list(range(nodeCount))
    greedy_length = total_length(points, nodeCount, greedy_solution)
    print("Found greedy solution: ",greedy_solution)

    bestYet = greedy_length
    bestSol = copy(greedy_solution)

    all_lengths = [greedy_length]
    best_lengths = [greedy_length]

    temp_list = []

    solution = greedy_solution
    n_rounds = 1
    starting_temp = find_temp_scale(solution, points)
    for i in range(n_rounds):
        #shuffle(solution)
        #all_lengths.append(total_length(points, nodeCount, solution))
        #best_lengths.append(bestYet)
        print("starting round %d"%i)
        temp = starting_temp 
        n_steps = 20000000
        temp_decrease_factor =  (1. - 8./n_steps)
        for _ in range(n_steps):
            temp = temp*temp_decrease_factor
            temp_list.append(temp)
            solution, delta_length = metropolis(solution, points, nodeCount, temp)
            #print(total_length(points, nodeCount, solution))
            current_length = all_lengths[-1] + delta_length
            all_lengths.append(current_length)
            if current_length < bestYet:
                bestYet = current_length
                bestSol = copy(solution)
            best_lengths.append(bestYet)

        print("best value yet: ",bestYet)

    plt.figure()
    plt.plot(all_lengths,'b')
    plt.plot(best_lengths,'r')

    plt.figure()
    plt.plot(temp_list,'b')

    # calculate the length of the tour
    obj = total_length(points, nodeCount, solution)
    plt.figure()
    draw_solution(points, nodeCount, bestSol, bestSol)

    #plt.show()

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

