"""
Write the testing function here.
"""

def find_relevant_tokens(data,num):
	relevant = []
	for elem in data:
		if elem[1]==num:
			relevant.append(elem)
	return relevant
	
def priors(data):
	prs = []
	tot = 0
	for i in range(10):
		rel = find_relevant_tokens(data,i)
		tot += len(rel)
		prs.append(len(rel))
	return (prs[0]/tot,prs[1]/tot,prs[2]/tot,prs[3]/tot,prs[4]/tot,
				prs[5]/tot,prs[6]/tot,prs[7]/tot,prs[8]/tot,prs[9]/tot)

def train(data):
	"""
	Trains the data and returns a 3D array (a list of matrices) of probabilites of each pixel in each class
	Think a heatmap of each class as a matrix
	:param data: the data from data parsing
	:return: 3D list of probabilities of each pixel of each class. 1- class, 2- y, row, 3- x, column
	"""
	probs = []
	k = 0.1
	for i in range(10):
		rel = find_relevant_tokens(data,i)
		matrix = []
		for row in range(32):
			row_matrix = []
			for col in range(32):
				occurences_of_1 = 0
				for tok in rel:
					if tok[0][row][col]==1:
						occurences_of_1+=1
				row_matrix.append((occurences_of_1+k)/(len(rel)+2*k))
			matrix.append(row_matrix)
		probs.append(matrix)
	return probs