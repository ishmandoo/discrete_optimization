#!/usr/bin/python
# -*- coding: utf-8 -*-

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

    items = []

    for i in range(1, item_count+1):
        line = lines[i]
        parts = line.split()
        items.append(Item(i-1, int(parts[0]), int(parts[1]),float(parts[0])/float(parts[1]),0))

    # a trivial greedy algorithm for filling the knapsack
    # it takes items in-order until the knapsack is full
    value = 0
    weight = 0
    taken = [0]*len(items)


    sorted_items = sorted(items, key=lambda item: -item.density)
    #assert(sorted_items[0].density >= sorted_items[1].density)

    def solve_knapsack(i, capacity, value, discrepancies_left):
        #print("%d \t %d \t %d \t %d"%(i,capacity,value,discrepancies_left))
        accept = reject = -1
        global best_result
        if i == len(sorted_items):
            #print("end of tree")
            best_result = max(best_result, value)
            return value
        
        upper_bound = value + compute_upper_bound(i, capacity)
        if upper_bound <= best_result:
            #print("pruning")
            return -1

        if sorted_items[i].weight <= capacity:
            if len(sorted_items)-i > discrepancies_left:
                accept = solve_knapsack(i+1, capacity-sorted_items[i].weight, value+sorted_items[i].value, discrepancies_left)

        if discrepancies_left > 0:
            reject = solve_knapsack(i+1, capacity, value, discrepancies_left-1)

        return max(accept, reject)



        '''
        if discrepancies_left == 0:
            reject = -1  
            if sorted_items[i].weight > capacity:
                print("0 disc left, can't accept next, too heavy")
                accept = -1     
            else:     
                print("0 disc left, can accept next")
                accept = solve_knapsack(i+1, capacity-sorted_items[i].weight, value+sorted_items[i].value, discrepancies_left)


        if len(sorted_items)-i >= discrepancies_left:
            #accept = -1
            print("too many disc left, must reject")            
            reject = solve_knapsack(i+1, capacity, value, discrepancies_left-1)

        return max(accept,reject)
'''




    def compute_upper_bound(i, capacity):
        value = 0
        for item in sorted_items[i:]:
            if item.weight <= capacity:
                value += item.value
                capacity -= item.weight
            else:
                value += item.density*capacity
                break
        return value

    print("i \tcap\tvalue\tdisc left")
    discUL = len(items)
    for disc in range(discUL+1):
        print("%d \t %d"%(disc, solve_knapsack(0, capacity, 0, disc)))
        print("")

    return("ASSSSSS%d"%best_result)

    



    """for item in items:
                    taken[item.index] = item.taken
                
                # prepare the solution in the specified output format
                output_data = str(value) + ' ' + str(0) + '\n'
                output_data += ' '.join(map(str, taken))
                return output_data"""


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)')






