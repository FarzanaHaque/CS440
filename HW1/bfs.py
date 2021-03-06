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

def bfs(maze,start):
	q = queue.Queue()
	q.put(start)
	parents = {}
	visited = set([start])
	dest = ()
	node_ex = 0

	while q:
		node = q.get()
		if maze[node[0]][node[1]]=='.':      #found solution
			dest = node
			break
		
		node_ex += 1

		if maze[node[0]][node[1]+1]!='%' and (node[0],node[1]+1) not in visited:   #add right
			visited.add((node[0],node[1]+1))
			q.put((node[0],node[1]+1))
			parents[(node[0],node[1]+1)]=node

		if maze[node[0]+1][node[1]]!='%' and (node[0]+1,node[1]) not in visited:    #down
			visited.add((node[0]+1,node[1]))
			q.put((node[0]+1,node[1]))
			parents[(node[0]+1,node[1])]=node

		if maze[node[0]][node[1]-1]!='%' and (node[0],node[1]-1) not in visited:   #left
			visited.add((node[0],node[1]-1))
			q.put((node[0],node[1]-1))
			parents[(node[0],node[1]-1)]=node

		if maze[node[0]-1][node[1]]!='%' and (node[0]-1,node[1]) not in visited:    #up
			visited.add((node[0]-1,node[1]))
			q.put((node[0]-1,node[1]))
			parents[(node[0]-1,node[1])]=node

	curr = dest
	solution=[dest]
	while curr!=start:
		curr=parents[curr]
		solution.append(curr)

	print("cost is %d" % len(solution))
	print("len of visited is %d" % node_ex)
	return solution

def write_sol(maze,solution):
	file = open('bfs_open_solution.txt','w')
	for node in solution:
		maze[node[0]][node[1]] = '.'
	for line in maze:
		str = ''.join(line)
		file.write("%s\n" %str)
	file.close()

#to use, change the input file, and specify the start position
maze = maze_parse("openmaze.txt")
sol = bfs(maze,(1,23))
write_sol(maze,sol)

		
