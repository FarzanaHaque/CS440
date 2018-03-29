"""
Write the testing function here.
"""


def find_relevant_tokens(data,num):
	relevant = []
	for elem in data:
		if elem[1]==num:
			relevant.append(elem)
	return relevant


def train(training_data):
	"""
	Trains the data and returns a 3D array (a list of matrices) of probabilites of each pixel in each class
	Think a heatmap of each class as a matrix
	:param data: the data from data parsing
	:return: 3D list of probabilities of each pixel of each class. 1- class, 2- y, row, 3- x, column
	"""
	return None