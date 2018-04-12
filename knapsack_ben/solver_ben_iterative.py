#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple
import sys
import threading
import queue

sys.setrecursionlimit(5000)
threading.stack_size(67108864) 

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
    
    sorted_items = sorted(items, key = lambda item: item.density)
    #sorted_items = items

    q = queue.LifoQueue()

    def evaluate(args):
        (i, taken, value, remaining) = args
        global best_taken, best_value
        if remaining < 0:
            return -1
        if i >= item_count:
            if value > best_value:
                best_value = value
                best_taken = taken
                #print("new best", value)
            return value
        item = sorted_items[i]
        #if (value + optimisticValue(i, capacity - weight)) <= best_value:
        if (value +  remaining * sorted_items[i].density) <= best_value:
            #print("prune",(value + optimisticValueSimple(i, capacity - weight)) )
            return -1

        
        q.put((i+1, taken + [item.index], value + item.value, remaining - item.weight))
        q.put((i+1, taken, value, remaining))


    q.put((0, [], 0, capacity))

    while not q.empty():
        evaluate(q.get())
    
    '''
    def dfs(i, taken, value, remaining):
        global best_taken, best_value
        #print(i,taken, value, weight)
        if remaining < 0:
            return -1
        if i >= item_count:
            if value > best_value:
                best_value = value
                best_taken = taken
                #print("new best", value)
            return value

        #if (value + optimisticValue(i, capacity - weight)) <= best_value:
        if (value +  remaining * sorted_items[i].density) <= best_value:
            #print("prune",(value + optimisticValueSimple(i, capacity - weight)) )
            return -1

        return max(
            dfs(i+1, taken + [i], value + sorted_items[i].value, remaining - sorted_items[i].weight), 
            dfs(i+1, taken, value, remaining)
            )
    '''


    taken = [0]*item_count
    for i in best_taken:
        taken[i] = 1
    
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

