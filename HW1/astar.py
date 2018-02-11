import queue

# cost of a move, should be heavier than manhattan distance
# found to be best value experimentally
c = 1.01

def maze_parse(path_to_file):
    file = open(path_to_file, "r")
    maze = []
    for line in file:
        x_line = []
        for c in line:
            if(c != '\n'):
                x_line.append(c)
        maze.append(x_line)
    file.close()
    return maze

def maze_print(maze):
   for line in maze:
      for c in line:
         print(c, end="")
      print()

def man_dist(x1, y1, x2, y2):
    return abs(abs(x2)-abs(x1)) + abs(abs(y2) - abs(y1))

def g(x1, y1, x2, y2, cost):
    return man_dist(x1, y1, x2, y2) + cost

def astar(maze, start, end):
    q = queue.PriorityQueue()
    q.put((g(end[0], end[1], start[0], start[1], 0), start[0], start[1]))
    parents = {}
    cost_map = {}
    cost_map[start] = 0
    visited = set([(start[0], start[1])])
    dest = ()
    min_cost = float('inf')
    node_ex = 0
    flag = 0
    while (not q.empty()):
        node = q.get()
        
        if(node[0] >= min_cost):    #already found best solution
            break

        if(node[1] == 14 and node[2] == 29):
 	        flag = 1
 
        #if(flag):
            #print((node[1], node[2]))

        if maze[node[1]][node[2]]=='.':    #found a solution
            if(node[0] < min_cost):
                dest = node
                min_cost = cost_map[(node[1], node[2])]
                continue
        node_ex += 1

        #make sure each node's parent is the least cost parent
        if maze[node[1]][node[2]+1]!='%' and (node[1],node[2]+1) not in visited:   #add right
            q.put((g(node[1], node[2]+1, end[0], end[1], (cost_map[(node[1], node[2])]+c)),  node[1], node[2]+1))
            if((node[1], node[2]+1) not in parents.keys() or cost_map[parents[(node[1],node[2]+1)]] > cost_map[(node[1], node[2])]+c):
                visited.add((node[1],node[2]+1))
                parents[(node[1],node[2]+1)]=(node[1], node[2])
                cost_map[(node[1],node[2]+1)] = cost_map[(node[1], node[2])]+c

        if maze[node[1]+1][node[2]]!='%' and (node[1]+1,node[2]) not in visited:    #down
            q.put((g(node[1]+1, node[2], end[0], end[1], (cost_map[(node[1], node[2])]+c)), node[1]+1, node[2]))
            if((node[1]+1, node[2]) not in parents.keys() or cost_map[parents[(node[1]+1,node[2])]] > cost_map[(node[1], node[2])]+c):
                visited.add((node[1]+1,node[2]))
                parents[(node[1]+1,node[2])]=(node[1], node[2])
                cost_map[(node[1]+1,node[2])] = cost_map[(node[1], node[2])]+c

        if maze[node[1]][node[2]-1]!='%' and (node[1],node[2]-1) not in visited:   #left
            q.put((g(node[1], node[2]-1, end[0], end[1], (cost_map[(node[1], node[2])]+c)), node[1], node[2]-1))
            if((node[1], node[2]-1) not in parents.keys() or cost_map[parents[(node[1],node[2]-1)]] > cost_map[(node[1], node[2])]+c):
                visited.add((node[1],node[2]-1))
                parents[(node[1],node[2]-1)]=(node[1], node[2])
                cost_map[(node[1],node[2]-1)] = cost_map[(node[1], node[2])]+c

        if maze[node[1]-1][node[2]]!='%' and (node[1]-1,node[2]) not in visited:    #up
            q.put((g(node[1]-1, node[2], end[0], end[1], (cost_map[(node[1], node[2])]+c)), node[1]-1, node[2]))
            if((node[1]-1, node[2]) not in parents.keys() or cost_map[parents[(node[1]-1,node[2])]] > cost_map[(node[1], node[2])]+c):
                visited.add((node[1]-1,node[2]))
                parents[(node[1]-1,node[2])]=(node[1], node[2])
                cost_map[(node[1]-1,node[2])] = cost_map[(node[1], node[2])]+c

    curr = (dest[1], dest[2])
    solution=[curr]
    while curr!=(start[0], start[1]):
        curr=parents[curr]
        solution.append(curr)

    print("cost is %d" % len(solution))
    print("len of visited %d" % node_ex)
    return solution

def write_sol(maze,solution):
    file = open('astar_med_solution.txt','w')
    for node in solution:
        maze[node[0]][node[1]] = '.'
    for line in maze:
        str = ''.join(line)
        file.write("%s\n" %str)
    file.close()

maze = maze_parse("medmaze.txt")
sol = astar(maze,(1,1),(21, 59))
write_sol(maze,sol)
