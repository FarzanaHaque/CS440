#Read in a file
#Read line by line to fill out a list of characters in a list of lists (2d) array
#print it out array

import queue
from collections import defaultdict
import math

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

def man_dist(p1, p2):
    return abs(abs(p1[0])-abs(p2[0])) + abs(abs(p1[1]) - abs(p1[1]))

def find_all_nodes(maze):
    nodes = []
    for row in range(0, len(maze)):
       for column in range(0, len(maze[row])):
          if(maze[row][column] == '.'):
              nodes.append((row, column))
    return nodes

def dict_for_graph(nodes):
    node_dict = {}
    for i in range(0, len(nodes)):
        node_dict[nodes[i]] = i
    return node_dict

def g(cost, maze, current):
    nodes = find_all_nodes(maze)
    node_dict = dict_for_graph(nodes)
    q = queue.PriorityQueue()

    for node_u in nodes:
        dist = man_dist(node_u, current)
        q.put(dist)
    
    return q.get() + cost

def astar(maze, start):
    q = queue.PriorityQueue()
    q.put((g(0, maze, start), start[0], start[1]))
    parents = {}
    cost_map = {}
    cost_map[start] = 0
    visited = set([(start[0], start[1])])
    dest = ()
    nodes_ex = 0
    total_cost = 0
    visit_counter = '1';
    old_start = start
    while (len(find_all_nodes(maze)) != 0):
        node = q.get()
        visited.add((node[1], node[2]))

        if maze[node[1]][node[2]]=='.':
            maze[node[1]][node[2]] = visit_counter
            visit_counter = chr(ord(visit_counter) + 1)
            if(ord(visit_counter) == ord(':')):
                visit_counter = 'a'

            curr = (node[1], node[2])
            solution=[curr]
            while curr!=(old_start[0], old_start[1]):
                curr=parents[curr]
                solution.append(curr)
            total_cost += (len(solution) - 1)

            q = queue.PriorityQueue()
            q.put((g(total_cost, maze, (node[1], node[2])), node[1], node[2]))
            parents = {}
            cost_map = {}
            cost_map[(node[1], node[2])] = 0
            visited = set([(node[1], node[2])])
            dest = ()
            old_start = (node[1], node[2])

        nodes_ex += 1

        if maze[node[1]][node[2]+1]!='%' and (node[1],node[2]+1) not in visited:   #add right
            q.put((g(cost_map[(node[1], node[2])]+1, maze, (node[1],node[2]+1)),  node[1], node[2]+1))
            if((node[1], node[2]+1) not in parents.keys() or cost_map[parents[(node[1],node[2]+1)]] > cost_map[(node[1], node[2])]+1):
                parents[(node[1],node[2]+1)]=(node[1], node[2])
                cost_map[(node[1],node[2]+1)] = cost_map[(node[1], node[2])]+1

        if maze[node[1]+1][node[2]]!='%' and (node[1]+1,node[2]) not in visited:    #down
            q.put((g(cost_map[(node[1], node[2])]+1, maze, (node[1]+1,node[2])), node[1]+1, node[2]))
            if((node[1]+1, node[2]) not in parents.keys() or cost_map[parents[(node[1]+1,node[2])]] > cost_map[(node[1], node[2])]+1):
                parents[(node[1]+1,node[2])]=(node[1], node[2])
                cost_map[(node[1]+1,node[2])] = cost_map[(node[1], node[2])]+1

        if maze[node[1]][node[2]-1]!='%' and (node[1],node[2]-1) not in visited:   #left
            q.put((g(cost_map[(node[1], node[2])]+1, maze, (node[1],node[2]-1)), node[1], node[2]-1))
            if((node[1], node[2]-1) not in parents.keys() or cost_map[parents[(node[1],node[2]-1)]] > cost_map[(node[1], node[2])]+1):
                parents[(node[1],node[2]-1)]=(node[1], node[2])
                cost_map[(node[1],node[2]-1)] = cost_map[(node[1], node[2])]+1

        if maze[node[1]-1][node[2]]!='%' and (node[1]-1,node[2]) not in visited:    #up
            q.put((g(cost_map[(node[1], node[2])]+1, maze, (node[1]-1,node[2])), node[1]-1, node[2]))
            if((node[1]-1, node[2]) not in parents.keys() or cost_map[parents[(node[1]-1,node[2])]] > cost_map[(node[1], node[2])]+1):
                parents[(node[1]-1,node[2])]=(node[1], node[2])
                cost_map[(node[1]-1,node[2])] = cost_map[(node[1], node[2])]+1

    print("cost is %d" % total_cost)
    print("Nodes Expanded is %d" % nodes_ex)

maze = maze_parse("smallmaze12.txt")
# tiny is (4,4)
# small is (1,7)
# med is (8, 25)
sol = astar(maze,(1,7))
maze_print(maze)
