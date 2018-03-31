"""
Tester function matching 1.1 testing
"""
import math



def test(trained_data, test_data):
	"""
	Classifies all the data given the trained_data from training.
	:param trained_data: the 3d list returned from training. See training for exact specs
	:param test_data: the data to test the trained NBC against
	:return: 1d array matching the data from data_parser
	log P(class) + log P(f1,1 | class) + log P(f1,2 | class) + ... + log P(f28,28 | class)

After you compute the above decision function values for all ten classes for every test image, you will use them for MAP classification.
	"""

for tups in test_data:



numprob=[0,0,0,0,0,0,0,0,0,0]
for h in range 10:
	for i in range 32:
		for j in range 32:
			numprob[h]=math.log1p(trained_data[h][i][j])+numprob[h]
	numprob[h]+=math.log1p(prior(h))


	return None
