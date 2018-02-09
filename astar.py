#Read in a file
#Read line by line to fill out a list of characters in a list of lists (2d) array
#print it out array

import queue

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
    while q:
        node = q.get()
        print(node) # node is (cost, y, x)
        visited.add((node[1], node[2]))
        if maze[node[1]][node[2]]=='.':
            dest = node
            break

        if maze[node[1]][node[2]+1]!='%' and (node[1],node[2]+1) not in visited:   #add right
            q.put((g(node[1], node[2]+1, end[0], end[1], cost_map[(node[1], node[2])]+1),  node[1], node[2]+1))
            parents[(node[1],node[2]+1)]=(node[1], node[2])
            cost_map[(node[1],node[2]+1)] = cost_map[(node[1], node[2])]+1
            
        if maze[node[1]+1][node[2]]!='%' and (node[1]+1,node[2]) not in visited:    #down
            q.put((g(node[1]+1, node[2], end[0], end[1], cost_map[(node[1], node[2])]+1), node[1]+1, node[2]))
            parents[(node[1]+1,node[2])]=(node[1], node[2])
            cost_map[(node[1]+1,node[2])] = cost_map[(node[1], node[2])]+1
            
        if maze[node[1]][node[2]-1]!='%' and (node[1],node[2]-1) not in visited:   #left
            q.put((g(node[1], node[2]-1, end[0], end[1], cost_map[(node[1], node[2])]+1), node[1], node[2]-1))
            parents[(node[1],node[2]-1)]=(node[1], node[2])
            cost_map[(node[1],node[2]-1)] = cost_map[(node[1], node[2])]+1
            
        if maze[node[1]-1][node[2]]!='%' and (node[1]-1,node[2]) not in visited:    #up
            q.put((g(node[1]-1, node[2], end[0], end[1], cost_map[(node[1], node[2])]+1), node[1]-1, node[2]))
            parents[(node[1]-1,node[2])]=(node[1], node[2])
            cost_map[(node[1]-1,node[2])] = cost_map[(node[1], node[2])]+1
            
    curr = (dest[1], dest[2])
    solution=[curr]
    while curr!=(start[0], start[1]):
        curr=parents[curr]
        solution.append(curr)
    
    print("cost is %d" % len(solution))
    print("nodes expanded is %d" % len(parents))
    return solution

def write_sol(maze,solution):
    file = open('solution.txt','w')
    for node in solution:
        maze[node[0]][node[1]] = '.'
    for line in maze:
        str = ''.join(line)
        file.write("%s\n" %str)
    file.close()
    
maze = maze_parse("medmaze.txt")
sol = astar(maze,(1,1), (21,59))
write_sol(maze,sol)

        
