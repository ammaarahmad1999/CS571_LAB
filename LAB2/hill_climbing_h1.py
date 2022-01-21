import heapq
import copy
import random
import time
from itertools import chain


def readInput(filename):
    '''This function reads the initial cur and the final cur from the provided filename'''

    # Read all the contents of the file
    with open(filename, 'r') as fi:
        data = fi.read()

    # Split around newline characters
    data = data.split('\n')

    # Split around spaces
    for i in range(len(data)):
        data[i] = data[i].split()

    data2 = list()

    # Remove empty lines
    for i in range(len(data)):
        if len(data[i]) > 0:
            data2.append(data[i])

    # Extract initial cur and final cur
    src = data2[0:3]
    dest = data2[3:6]
    
    src = list(chain.from_iterable(src))
    dest = list(chain.from_iterable(dest))
    
    return src, dest


def normalize(arr):
    '''This function extracts the position of Blank and replaces B with 0 and Ti with i'''
    for j in range(len(arr)):
        if arr[j] == 'B':
            arr[j] = 0
        else:
            arr[j] = int(arr[j][1])
    return arr


def h1(cur, dest):
    '''This function calculates number of misplaced tiles'''
    
    res = 0
    for i in range(9):
        if(cur[i] == dest[i]):
        	res += 1
    return res

def hash_value(arr):
    '''Calculate the hash value of the matrix'''
	power = 1
	value = 0
	for x in arr:
		value += x*power
		power = power*9
	return value



def print_aux(a):
    '''This function helps in pretty-printing the solution'''
    for i in range(3):
        for j in range(3):
            c = a[i*3+j]
            if c == 0:
                print('B  ', end='', sep='')
            else:
                print('T', c, ' ', end='', sep='')
        print() # change line for next row
   
    print()
    return



def print_sol(src, dest, hash_map):
    '''This function prints the path to the solution'''
    if src == dest: # destination reached
        print_aux(src)
        return
    value = hash_value(dest)
    temp = reverse_hash(hash_map[value][0])
    print_sol(src, temp, hash_map) # do a recursive call
    print_aux(dest)

    return


def print_results(src, dest, hash_map, cnt, start, end, last_cur):
    '''This function prints the final results'''

    tmp = hash_value(dest)

    if tmp in hash_map:     # if solution is found
        print('Solution found!')

        print('Start cur: ')
        print_aux(src)

        print('Goal Sate: ')
        print_aux(dest)

        print('Total number of states explored =', cnt)

        res = hash_map[tmp]

        print('Total number of states to optimal path =', res[1]+1)

        print('Optimal path: ')
        print_sol(src, tmp, hash_map)

        print('Optimal path cost =', res[1])

        print('Time taken for execution =', '%.6f'%(end-start), 'seconds')


    else:       # if failed to find a solution
    
        print('Found a local maxima')
        print_aux(last_cur)

        print('Start cur: ')
        print_aux(src)

        print('Goal Sate: ')
        print_aux(dest)
        
        print('Total number of states explored before termination =', cnt)

    return



def hill_climbing(src, dest, heu):
    '''This function solves the 8-puzzle problem using hill-climbing algorithm with some sideways movements
    allowed. heu is the heuristic function to be used'''
    
    hash_map = dict()

    cnt = 0     # to store number of explored curs
    
    # first component is the predecessor, second component is the distance from the source cur
    temp = hash_value(src)
    hash_map[temp] = ([], 0)
    depth = 0

    cur = copy.deepcopy(src)
    val = -heu(cur, dest)

    if src == dest:     # already at the goal cur
        return cur, hash_map, cnt

    max_sideways = 10   # number of maximum sideways movement allowed
    side_cnt = 0        # count of sideways movements at this point   

    while True:     # run while we are able to find better neighbours

        cnt += 1
        depth += 1

        if src == dest:     # GOAL cur reached
            return cur, hash_map, cnt

        # Locate the blank
        x, y = 0, 0
        for i in range(9):
            if(cur[i] == 0):
                x = i//3
                y = i%3
                break
        
        # Shift the blank in all 4 directions, if possible
        change = [[1, 0], [-1, 0], [0, 1], [0, -1]]
        
        new_cur = list()
        a = val

        for i, shift in enumerate(change):

            nx = x + shift[0]
            ny = y + shift[1]

            if nx < 0 or ny < 0 or nx > 2 or ny > 2:
                # invalid shift of blank
                continue
            
            # shiting the blank
            cur[x*3+y], cur[nx*3+ny] = cur[nx*3+ny], cur[x*3+y]
            
            tmp = hash_value(cur)

            if tmp not in hash_map: 			# a new cur that was not seen before
                tmp_val = -heu(cur, dest)
                a = max(a, tmp_val)
                if tmp_val >= val:
                    new_cur.append((nx, ny, tmp_val))

            cur[x*3+y], cur[nx*3+ny] = cur[nx*3+ny], cur[x*3+y]

        # all the 'equal or better' neighbours are in nei[] list
        
        if len(new_cur) == 0:       # no new neighbours found
            return cur, hash_map, cnt
        
        else:       
            #random.shuffle(new_cur)
            if a == val:    # a flat region detected; hope it's a shoulder
                if side_cnt == max_sideways:    # maximum sideways tried; very likely that it's a plateau
                    return cur, hash_map, cnt
                
                else:   # choose one of the neighbours to move to
                    side_cnt += 1
                    
                    nx, ny, val = new_cur[0]

                    tmp = hash_value(cur)
                    
                    cur[x*3+y], cur[nx*3+ny] = cur[nx*3+ny], cur[x*3+y]
                    
                    hash_map[hash_value(cur)] = (tmp, depth)
            
            else:   # better neighbours found
                side_cnt = 0

                best_cur = []
                
                for i, z in enumerate(new_cur):
                    if z[2] == a:
                        best_cur = z
                        break

                nx, ny, val = best_cur
                
                #print(nx, ny, val)

                tmp = hash_value(cur)

                cur[x*3+y], cur[nx*3+ny] = cur[nx*3+ny], cur[x*3+y]

                hash_map[hash_value(cur)] = (tmp, depth)




filename = input("Enter filename: ")    # take the filename as input

src, dest = readInput(filename)

src = normalize(src)
dest = normalize(dest)

start = time.time()

# solve with h1 as heuristic
last_cur, hash_map, cnt = hill_climbing(src, dest, h2)

end = time.time()

print_results(src, dest, hash_map, cnt, start, end, last_cur)
