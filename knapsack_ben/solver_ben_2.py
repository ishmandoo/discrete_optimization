#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple
import sys

sys.setrecursionlimit(2000)

Item = namedtuple("Item", ['index', 'value', 'weight', 'density'])


best_value = 0
best_taken = [] 

def solve_it(input_data):
    global best_value, best_taken

    best_value = 0
    best_taken = [] 

    # parse the input
    lines = input_data.split('\n')

    firstLine = lines[0].split()
    item_count = int(firstLine[0])
    capacity = int(firstLine[1])

    items = []

    for i in range(1, item_count+1):
        line = lines[i]
        parts = line.split()
        items.append(Item(i-1, int(parts[0]), int(parts[1]), float(parts[0]) / float(parts[1])))
    
    
    densities = [float(item.value)/item.weight for item in items]
    best_density_from = densities
    for i in range(item_count-1,-1,-1):
        if not i == item_count - 1:
            best_density_from[i] = max(best_density_from[i+1], densities[i])
    
    weights = [item.weight for item in items]
    smallest_from = weights
    for i in range(item_count-1,-1,-1):
        if not i == item_count - 1:
            smallest_from[i] = min(smallest_from[i+1], weights[i])

    def optimisticValue(i, remaining):
        last_i_used = i
        value = 0
        while i < item_count-1 and remaining > smallest_from[i]:
            item_to_consider = sorted_items[i]
            if item_to_consider.weight <= remaining:
                remaining -= item_to_consider.weight
                value += item_to_consider.value
                last_i_used = i
            i += 1
        if last_i_used + 1 < item_count:
            return value + (remaining * densities[last_i_used])
        else:
            return value

    sorted_items = sorted(items, key = lambda item: -item.density)
    #print sorted_items

    def dfs2(i, taken, value, weight):
        global best_taken, best_value
        if weight > capacity:
            return -1
        if i >= item_count:
            if value > best_value:
                best_value = value
                best_taken = taken
                print "new best", value
            return value

        if (value + optimisticValue(i, capacity - weight)) < best_value:
            #print "prune"
            return -1

        return max(
            dfs2(i+1, taken + [1], value + sorted_items[i].value, weight + sorted_items[i].weight), 
            dfs2(i+1, taken + [0], value, weight)
            )

    sol = dfs2(0, [], 0, 0)


    taken = [0]*item_count
    for i, item in enumerate(sorted_items):
        print len(best_taken)
        taken[item.index] = best_taken[i]
    
    # prepare the solution in the specified output format
    output_data = str(best_value) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, taken))
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

