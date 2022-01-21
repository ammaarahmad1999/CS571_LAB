import time
import copy
import numpy
import heapq
from itertools import chain


def normalize(arr):
    for j in range(len(arr)):
        if arr[j] == 'B':
            arr[j] = 0
        else:
            arr[j] = int(arr[j][1])
    return arr

def hash_value(arr):
	power = 1
	value = 0
	#print(len(arr))
	for x in arr:
		value += x*power
		power = power*9
		#print(x, power)
	#print(value)
	return value

hash_value([0, 1, 2, 3, 4, 5, 6, 7, 8])
	
def reverse_hash(value):
	arr = []
	cnt = 9
	while (cnt):
		arr.append(value%9)
		value = value//9
		cnt -= 1
	
	return arr

def readInput(filename):
    # Read all the contents of the file
    with open(filename, 'r') as fi:
        data = fi.read()
    # Split around newline characters
    data = data.split('\n')
    # Split around spaces
    for i in range(len(data)):
        data[i] = data[i].split()

    # Remove empty lines
    for i in range(len(data)-1):
        if len(data[i]) == 0:
            data = data[:i] + data[i+1:]
    # Extract initial state and final state
    src = data[0:3]
    dest = data[3:6]

    src = list(chain.from_iterable(src))
    dest = list(chain.from_iterable(dest))

    return src, dest


def print_aux(a):
    for i in range(3):
        for j in range(3):
            c = a[i*3+j]
            if c == 0:
                print('B  ', end='', sep='')
            else:
                print('T', c, ' ', end='', sep='')
        print()  # change line for next row

    print()
    return


def h2(cur, dest):
    '''This function calculates the Manhattan distance of tiles from their required positions'''
    sum = 0

    for i in range(9):
        for j in range(9):
            if(cur[i] == dest[j]):
            	sum += abs(i/3-j/3) + abs(i%3-j%3)

    return sum                    

def a_star(src, dest, heu):
    '''This function solves the 8-puzzle problem using A* search'''

    hash = dict()   # a hashmap to store distance and predecessors for constructing paths later
    dead = set()    # to store the dead states
    pq = list()     # a priority queue to store the frontier
    heapq.heapify(pq)

    cnt = 0 # to store the count of states explored
    
    temp = hash_value(src)
    
    hash[temp] = ([], 0) # first component is the predecessor, second compoment is the distance from the source state
    heapq.heappush(pq, (0+heu(src, dest), temp))

    
    if src == dest:
        return hash, cnt

    while len(pq) > 0:  # Run until destination reached or all states explored
        
        # Pop a state from the priority queue
        a = heapq.heappop(pq)
        cur = a[1]  # current state

        # If this state has already been explored, then skip
        if cur in dead:
            continue
        
        cnt += 1

        # Add this state to the list of already-explored states
        dead.add(cur)
        t1, t2 = hash[cur]
        
        state = reverse_hash(cur)

        if state == dest:   # destination reached, return
            return hash, cnt

        # Locate the 0 (blank)
        x , y = 0, 0
        
        for i in range(9):
            if(state[i] == 0):
                x = i//3
                y = i%3
                break

        # Shift the blank in all 4 directions, if possible
        change = [[1, 0], [-1, 0], [0, 1], [0, -1]]

        for i, shift in enumerate(change):
            
            
            nx = x + shift[0]
            ny = y + shift[1]

            if nx < 0 or ny < 0 or nx > 2 or ny > 2:
                # invalid shift of the blank
                continue
            
            # Swap the blank and the T-cell to generate a new state
            state[x*3+y], state[nx*3+ny] = state[nx*3+ny], state[x*3+y]
            
            temp = hash_value(state)

            if temp in dead: # The generated state has already been explored
                pass
            
            elif temp not in hash:   # The generated state is being seen for the first time
                hash[temp] = (cur, 1+t2)
                heapq.heappush(pq, (1+t2+heu(state, dest), temp))

            else:
                q1, q2 = hash[temp]

                if q2 > 1+t2:   # The generated state was seen before, but has not been explored and this is a shorter path
                                # to it from the source state
                    hash[temp] = (cur, 1+t2)
                    heapq.heappush(pq, (1+t2+heu(state, dest), temp))
            
            state[x*3+y], state[nx*3+ny] = state[nx*3+ny], state[x*3+y]


    # end of while() loop

    return hash, cnt

def print_sol(src, dest, hash):
    '''This function prints the path to the solution'''
    if src == dest:
        print_aux(src)
        return
    value = hash_value(dest)
    temp = reverse_hash(hash[value][0])
    print_sol(src, temp, hash)
    print_aux(dest)

    return


def print_results(src, dest, hash, cnt):
    tmp = hash_value(dest)
    if tmp in hash:
        print('Solution found!')
        print('Start state: ')
        print_aux(src)
        print('Goal Sate: ')
        print_aux(dest)
        print('Total number of states explored =', cnt)
        res = hash[tmp]
        print('Total number of states to optimal path =', res[1]+1)
        print('Optimal path: ')
        print_sol(src, dest, hash)
        print('Optimal path cost =', res[1])
    else:
        print('No solution found!')
        print('Start state: ')
        print_aux(src)
        print('Goal Sate: ')
        print_aux(dest)
        print('Total number of states explored before termination =', cnt)

    return


fileName = input("Enter the filename: ")
src, dest = readInput(fileName)
src = normalize(src)
dest = normalize(dest)
start = time.time()
hash, cnt = a_star(src, dest, h2)
end = time.time()
print_results(src, dest, hash, cnt)

print('Time taken for execution =', '%.6f' % (end-start), 'seconds')

exit(0)
