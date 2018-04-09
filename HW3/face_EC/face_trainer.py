"""
Write the testing function here.
"""
def find_relevant_tokens(data,num):
	relevant = []
	for elem in data:
		if elem[1]==num:
			relevant.append(elem)
	return relevant


def priors(data):#returns 2 element array, 1st is P(zero) 2nd is P(one) meaning non face and face
    zero_count=0
    one_count=0
    for elem in data:
        if elem[1]==0:
            zero_count+=1
        else:
            one_count+=1
    return(zero_count/(zero_count+one_count), one_count/(zero_count+one_count))


def train(data):
    """
    Trains the data and returns a 3D array (a list of matrices) of probabilites of each pixel in each class
    Think a heatmap of each class as a matrix
    :param data: the data from data parsing
    :return: 3D list of probabilities of each pixel of each class. 1- class, 2- y, row, 3- x, column
    """
    probs = []
    k = .1
    for i in range(2):
        rel = find_relevant_tokens(data, i)
        matrix = []
        for row in range(70):
            row_matrix = []
            for col in range(60):
                occurences_of_hash = 0
                for tok in rel:
                    if tok[0][row][col] == "#":
                        occurences_of_hash += 1
                row_matrix.append((occurences_of_hash + k) / (len(rel) + 2 * k))
            matrix.append(row_matrix)
        probs.append(matrix)
    return probs