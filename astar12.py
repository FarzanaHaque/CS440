#Read in a file
#Read line by line to fill out a list of characters in a list of lists (2d) array
#print it out array

import queue
from collections import defaultdict
import math

#From https://www.geeksforgeeks.org/greedy-algorithms-set-2-kruskals-minimum-spanning-tree-mst/
# Python program for Kruskal's algorithm to find
# Minimum Spanning Tree of a given connected,
# undirected and weighted graph
#Class to represent a graph
class Graph:
    def __init__(self,vertices):
        self.V= vertices #No. of vertices
        self.graph = [] # default dictionary
                                # to store graph

    # function to add an edge to graph
    def addEdge(self,u,v,w):
        self.graph.append([u,v,w])

    # A utility function to find set of an element i
    # (uses path compression technique)
    def find(self, parent, i):
        if parent[i] == i:
            return i
        return self.find(parent, parent[i])

    # A function that does union of two sets of x and y
    # (uses union by rank)
    def union(self, parent, rank, x, y):
        xroot = self.find(parent, x)
        yroot = self.find(parent, y)

        # Attach smaller rank tree under root of
        # high rank tree (Union by Rank)
        if rank[xroot] < rank[yroot]:
            parent[xroot] = yroot
        elif rank[xroot] > rank[yroot]:
            parent[yroot] = xroot

        # If ranks are same, then make one as root
        # and increment its rank by one
        else :
            parent[yroot] = xroot
            rank[xroot] += 1

    # The main function to construct MST using Kruskal's
        # algorithm
    def KruskalMST(self):

        result =[] #This will store the resultant MST

        i = 0 # An index variable, used for sorted edges
        e = 0 # An index variable, used for result[]

            # Step 1: Sort all the edges in non-decreasing
                # order of their
                # weight. If we are not allowed to change the
                # given graph, we can create a copy of graph
        self.graph = sorted(self.graph,key=lambda item: item[2])

        parent = [] ; rank = []

        # Create V subsets with single elements
        for node in range(self.V):
            parent.append(node)
            rank.append(0)

        # Number of edges to be taken is equal to V-1
        while e < self.V -1 :

            # Step 2: Pick the smallest edge and increment
                    # the index for next iteration
            u,v,w = self.graph[i]

            i = i + 1
            x = self.find(parent, u)
            y = self.find(parent ,v)

            # If including this edge does't cause cycle,
                        # include it in result and increment the index
                        # of result for next edge
            if x != y:
                e = e + 1
                result.append([u,v,w])
                self.union(parent, rank, x, y)
            # Else discard the edge

        # print the contents of result[] to display the built MST
        sum = 0
        #print "Following are the edges in the constructed MST"
        for u,v,weight in result:
            #print str(u) + " -- " + str(v) + " == " + str(weight)
            #print ("%d -- %d == %d" % (u,v,weight))
            sum += weight
        return sum

#This code is contributed by Neelam Yadav
#End from https://www.geeksforgeeks.org/greedy-algorithms-set-2-kruskals-minimum-spanning-tree-mst/


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
    nodes.append(current)
    nodes = set(nodes)
    nodes = list(nodes)
    node_dict = dict_for_graph(nodes)

    g = Graph(len(nodes))
    for node_u in nodes:
        for node_v in nodes:
            dist = man_dist(node_u, node_v)
            if(node_u != node_v):
                g.addEdge(node_dict[node_u], node_dict[node_v], dist)

    sum = g.KruskalMST()
    return sum + cost

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
        #visited.add((node[1], node[2]))

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
            visited.add((node[1], node[2])+1)
			q.put((g(cost_map[(node[1], node[2])]+1, maze, (node[1],node[2]+1)),  node[1], node[2]+1))
            if((node[1], node[2]+1) not in parents.keys() or cost_map[parents[(node[1],node[2]+1)]] > cost_map[(node[1], node[2])]+1):
                parents[(node[1],node[2]+1)]=(node[1], node[2])
                cost_map[(node[1],node[2]+1)] = cost_map[(node[1], node[2])]+1

        if maze[node[1]+1][node[2]]!='%' and (node[1]+1,node[2]) not in visited:    #down
            visited.add((node[1]+1, node[2]))
			q.put((g(cost_map[(node[1], node[2])]+1, maze, (node[1]+1,node[2])), node[1]+1, node[2]))
            if((node[1]+1, node[2]) not in parents.keys() or cost_map[parents[(node[1]+1,node[2])]] > cost_map[(node[1], node[2])]+1):
                parents[(node[1]+1,node[2])]=(node[1], node[2])
                cost_map[(node[1]+1,node[2])] = cost_map[(node[1], node[2])]+1

        if maze[node[1]][node[2]-1]!='%' and (node[1],node[2]-1) not in visited:   #left
            visited.add((node[1], node[2]-1))
			q.put((g(cost_map[(node[1], node[2])]+1, maze, (node[1],node[2]-1)), node[1], node[2]-1))
            if((node[1], node[2]-1) not in parents.keys() or cost_map[parents[(node[1],node[2]-1)]] > cost_map[(node[1], node[2])]+1):
                parents[(node[1],node[2]-1)]=(node[1], node[2])
                cost_map[(node[1],node[2]-1)] = cost_map[(node[1], node[2])]+1

        if maze[node[1]-1][node[2]]!='%' and (node[1]-1,node[2]) not in visited:    #up
            visited.add((node[1]-1, node[2]))
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