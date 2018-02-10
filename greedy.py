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

def greedy(maze, start, end):
    q = queue.PriorityQueue()
    q.put((man_dist(end[0], end[1], start[0], start[1]), start[0], start[1]))
    parents = {}
    visited = set([(man_dist(end[0], end[1], start[0], start[1]), start[0], start[1])])
    dest = ()
    nodes_ex = 0
    while q:
        node = q.get()
        #print(node)
        visited.add(node)
        if maze[node[1]][node[2]]=='.':
            dest = node
            break
        nodes_ex += 1
        if maze[node[1]][node[2]+1]!='%' and (man_dist(node[1], node[2]+1, end[0], end[1]), node[1],node[2]+1) not in visited:   #add right
            q.put((man_dist(node[1], node[2]+1, end[0], end[1]), node[1],node[2]+1))
            parents[(man_dist(node[1], node[2]+1, end[0], end[1]), node[1],node[2]+1)]=node

        if maze[node[1]+1][node[2]]!='%' and (man_dist(node[1]+1, node[2], end[0], end[1]), node[1]+1,node[2]) not in visited:    #down
            q.put((man_dist(node[1]+1, node[2], end[0], end[1]), node[1]+1,node[2]))
            parents[(man_dist(node[1]+1, node[2], end[0], end[1]), node[1]+1,node[2])]=node

        if maze[node[1]][node[2]-1]!='%' and (man_dist(node[1], node[2]-1, end[0], end[1]), node[1],node[2]-1) not in visited:   #left
            q.put((man_dist(node[1], node[2]-1, end[0], end[1]), node[1],node[2]-1))
            parents[(man_dist(node[1], node[2]-1, end[0], end[1]), node[1],node[2]-1)]=node

        if maze[node[1]-1][node[2]]!='%' and (man_dist(node[1]-1, node[2], end[0], end[1]), node[1]-1,node[2]) not in visited:    #up
            q.put((man_dist(node[1]-1, node[2], end[0], end[1]), node[1]-1,node[2]))
            parents[(man_dist(node[1]-1, node[2], end[0], end[1]), node[1]-1,node[2])]=node

    curr = dest
    solution=[dest]
    while curr!=(man_dist(end[0], end[1], start[0], start[1]), start[0], start[1]):
        curr=parents[curr]
        solution.append(curr)

    print("cost is %d" % len(solution))
    print("nodes expanded is %d" % len(parents))
    print("new estimate is %d" % nodes_ex)
    return solution

def write_sol(maze,solution):
    file = open('med_greedy_solution.txt','w')
    for node in solution:
        maze[node[1]][node[2]] = '.'
    for line in maze:
        str = ''.join(line)
        file.write("%s\n" %str)
    file.close()

maze = maze_parse("medmaze.txt")
sol = greedy(maze,(1,1), (21,59))
write_sol(maze,sol)
