#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple
Item = namedtuple("Item", ['index', 'value', 'weight', 'density'])

Solution = namedtuple("Solution", ['taken', 'value', 'weight'])

best_value = 0
best_taken = []
def solve_it(input_data):
    # Modify this code to run your optimization algorithm

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

    sorted_items = sorted(items, key = lambda item: -item.density)
    #print sorted_items

    def dfs(i, taken, value, weight):
        global best_value
        if weight > capacity:
            return Solution(taken, -1, weight)
        if i >= item_count:
            if value > best_value:
                print "new best", value
            best_value = max(best_value, value)
            return Solution(taken, value, weight)

        if (value + ((capacity - weight) * best_density_from[i])) < best_value:
            #print "prune"
            return Solution(taken, -1, weight)
        return max(
            dfs(i+1, taken + [1], value + items[i].value, weight + items[i].weight), 
            dfs(i+1, taken + [0], value, weight), 
            key=lambda sol: sol.value)

    #sol = dfs(0, [], 0, 0)
    #best_value = sol.value
    #best_taken = sol.taken    

    def dfs2(i, taken, value, weight):
        global best_value, best_taken
        if weight > capacity:
            return -1
        if i >= item_count:
            if value > best_value:
                print "new best", value
            best_value = max(best_value, value)
            best_taken = taken
            return value

        if (value + ((capacity - weight) * best_density_from[i])) < best_value:
            #print "prune"
            return -1
        return max(
            dfs2(i+1, taken + [1], value + items[i].value, weight + items[i].weight), 
            dfs2(i+1, taken + [0], value, weight)
            )

    sol = dfs2(0, [], 0, 0)
    
    # prepare the solution in the specified output format
    output_data = str(best_value) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, best_taken))
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

