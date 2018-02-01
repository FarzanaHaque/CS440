#Read in a file
#Read line by line to fill out a list of characters in a list of lists (2d) array
#print it out array

def maze_parse(path_to_file):
   file = open(path_to_file, "r")
   maze = []
   for line in file:
      x_line = []
      for c in line:
         if(c != '\n'):
            x_line.append(c)        
      maze.append(x_line)
   return maze

def maze_print(maze):
   for line in maze:
      for c in line:
         print(c, end="")
      print()
      
# maze = maze_parse("medmaze.txt")
# print(maze[1][1])
# print(maze[21][59])

# maze_print(maze)
