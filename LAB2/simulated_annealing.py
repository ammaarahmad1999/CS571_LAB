import heapq
import copy
import random
import time
import math
from itertools import chain

def readInput(filename):
    '''This function reads the initial state and the final state from the provided filename'''

    # Read all the contents of the file
    with open(filename, 'r') as fi:
        data = fi.read()

    # Split around newline characters
    data = data.split('\n')

    # Split around spaces
    for i in range(len(data)):
        data[i] = data[i].split()

    data2 = []

    # Remove empty lines
    for i in range(len(data)):
        if len(data[i]) > 0:
            data2.append(data[i])

    # Extract initial state and final state
    src = data2[0:3]
    dest = data2[3:6]
    
    src = list(chain.from_iterable(src))
    dest = list(chain.from_iterable(dest))
    
    return src, dest

def normalize(arr):
    for j in range(len(arr)):
        if arr[j] == 'B':
            arr[j] = 0
        else:
            arr[j] = int(arr[j][1])
    return arr


def h1(cur, dest, isTile):
    '''This function calculates number of misplaced tiles'''
    
    res = 0
    for i in range(9):
        if cur[i] == 0 and isTile == False:
                continue
        if(cur[i] == dest[i]):
        	res += 1
    return res


def h2(cur, dest, isTile):
    '''This function calculates the Manhattan distance of tiles from their required positions'''
    sum = 0

    for i in range(9):
        for j in range(9):
            if cur[i] == 0 and isTile == False:
                continue
            if(cur[i] == dest[j]):
            	sum += abs(i/3-j/3) + abs(i%3-j%3)

    return sum                    

def h3(cur, dest, isTile):
    return h1(cur, dest, isTile) * h2(cur, dest, isTile)
    
    
def hash_value(arr):
	power = 1
	value = 0
	for x in arr:
		value += x*power
		power = power*9
	return value

def reverse_hash(value):
	arr = []
	cnt = 9
	while (cnt):
		arr.append(value%9)
		value = value//9
		cnt -= 1
	
	return arr
	
## Printer functions ahead

def print_aux(fi, a):
    '''This function helps in pretty-printing the solution'''
    for i in range(3):
        for j in range(3):
            c = a[i*3+j]
            if c == 0:
                print('B  ', end='', sep='', file=fi)
            else:
                print('T', c, ' ', end='', sep='', file=fi)
        print(file=fi)  # change line for next row
   
    print(file=fi)
    return

## Probability-relaed functions ahead

def prob_expo(e, t):
    '''This function returns value for considering exponential probability'''
    e = float(e)
    t = float(t)
    return math.exp(-e/t)


def prob_normal(e, t):
    '''This function returns value for considering standard normal probability'''
    e = float(e)
    t = float(t)

    return (1/(math.sqrt(2*math.pi))) * math.exp(-math.pow(e/t, 2)/2)


## Cooling functions ahead

epsilon = 1e-3

def linear(t):
    t = float(t)
    t -= 0.1

    if t <= epsilon:
        return 0

    return t

def exponential(t):
    t = float(t)
    t -= t/2

    if t <= epsilon:
        return 0

    return t

## The MAIN search function ahead

def simulated_annealing(src, dest, temp, heu, change, prob, cool, isTile):
    '''This function solves the 8-puzzle problem using simulated annealing'''

    chain = []  # to store the path to the solution, if found
    dead = set()    # to store the set of explored states

    tmp = hash_value(src)

    chain.append(tmp)

    if src == dest:     # if source and destination are same
        return chain, len(dead)

    cur = copy.deepcopy(src)
    dead.add(tmp)

    # Start the process
    while temp > 0:

        if cur == dest:     # Goal reached
            return chain, len(dead)
        
        # Locate the blank
        x, y = 0, 0
        for i in range(9):
            if(cur[i] == 0):
                x = i//3
                y = i%3
                break

        
        # Generate all the neighbours according to the given neighbourhood-generating function
        for i, shift in enumerate(change):
        
            nx = x + shift[0]
            ny = y + shift[1]

            if nx < 0 or ny < 0 or nx > 2 or ny > 2:
                # invalid shift of blank
                continue
            
            # energy of the current state
            e_cur = -heu(cur, dest, isTile)
            
            # shiting the blank
            cur[x*3+y], cur[nx*3+ny] = cur[nx*3+ny], cur[x*3+y]
            # energy of the neighbour
            e_next = -heu(cur, dest, isTile)
            
            diff = e_next - e_cur   # energy difference

            tmp = hash_value(cur)
            if tmp not in dead:
                dead.add(tmp)

            if diff > 0:   # move to the better neighbour
                chain.append(hash_value(cur))
                pass

            else:
                p = prob(1, temp)    # find the probability
                a = random.random()

                if a <= p:  # accept this neighbour
                    chain.append(hash_value(cur))
                    pass
                else:       # don't accept this neighbour
                    cur[x*3+y], cur[nx*3+ny] = cur[nx*3+ny], cur[x*3+y]

            break


        # Apply the cooling function
        temp = cool(temp)

    return chain, len(dead)

# Get the file comtiang the start state and the goal state
filename = input("Enter filename containing the start state and the goal state: ")

src, dest = readInput(filename)

src = normalize(src)
dest = normalize(dest)

# Get the intial starting temperature
temp = int(input("Enter the starting temperature (must be greater than 0): "))

# Get the heuristic
print('Consider the following heuristic functions - ')
print('1. h1(n) = number of displaced tiles')
print('2. h2(n) = total Manhattan distance')
print('3. h3(n) = h1(n)*h2(n)')

heu_option = int(input('Choose one option (1 or 2 or 3): '))

heu = None
if heu_option == 1:
    heu = h1
elif heu_option == 2:
    heu = h2
else:
    heu = h3


# Get the neighbourhood generating function
print('Consider the following neighbourhood-generating functions - ')
print('\t1. In order UP, RIGHT, DOWN, LEFT')
print('\t2. In order UP, LEFT, DOWN, RIGHT')

nei_generate_option = int(input('Select one option (1 or 2): '))

change = []
if nei_generate_option == 1:
    change = [[-1, 0], [0, 1], [1, 0], [0, -1]]
else:
    change = [[-1, 0], [0, -1], [1, 0], [0, 1]]



# Get the probability function
print('Consider the following probability functions - ')
print('\t1. Negative exponential')
print('\t2. Standard normal distribution')

prob_option = int(input('Select one option (1 or 2): '))


prob = None
if prob_option == 1:
    prob = prob_expo
else:
    prob = prob_normal


# Get the cooling function
print('Consider the following cooling functions - ')
print('1. linear cooling')
print('2. exponential cooling')

cooling_option = int(input('Select one option (1 or 2): '))

cool = None
if cooling_option == 1:
    cool = linear
else:
    cool = exponential


# Ask if blank tile is considered as another tile
isTile = int(input('Is blank tile considered as another tile? (0/1): '))
isTile = bool(isTile)


# Solve the puzzle and note the time taken
start = time.time()
chain, cnt = simulated_annealing(src, dest, temp, heu, change, prob, cool, isTile)
end = time.time()



# Print the results
with open('output.txt', 'w') as fi:

    tmp = chain[len(chain)-1]

    if tmp != hash_value(dest):
        print('Solution not found', file=fi)
        print('Found a local maxima!', file=fi)
        print_aux(fi, reverse_hash(tmp))   

    else:
        print('Solution found!', file=fi)


    print('Heuristic chosen = ', file=fi, end='')
    if heu_option == 1:
        print('Number of displaced tiles', file=fi)
        print('The chosen heuristic is admissible\n', file=fi)

    elif heu_option == 2:
        print('Total Manhattan distance', file=fi)
        print('The chosen heurisitc is admissible\n', file=fi)
    
    else:
        print('h1(n) * h2(n)', file=fi)
        print('The chosen heuristic is not admissible\n', file=fi)
    

    print('Temperature chosen =', temp, file=fi)

    print('Cooling function chosen = ', file=fi, end='')
    if cooling_option == 1:
        print('Linear cooling', file=fi)
    else:
        print('Exponential cooling', file=fi)

    print('Start state: ', file=fi)
    print_aux(fi, src)

    print(file=fi)

    print('Goal state: ', file=fi)
    print_aux(fi, dest)

    if tmp == hash_value(dest):
        print('(Sub) Optimal path to success: ', file=fi)
        for a in chain:
            print_aux(fi, reverse_hash(a))


    print('Total number of states explored =', cnt, file=fi)

    print('Time amount of time taken =', '%.6f'%(end-start), 'seconds', file=fi)

