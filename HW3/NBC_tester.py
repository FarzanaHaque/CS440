"""
Tester function matching 1.1 testing
"""
import math
import NBC_trainer




def test(trained_data, test_data):
	"""
	Classifies all the data given the trained_data from training.
	:param trained_data: the 3d list returned from training. See training for exact specs
	:param test_data: the data to test the trained NBC against
	:return: 1d array matching the data from data_parser
	log P(class) + log P(f1,1 | class) + log P(f1,2 | class) + ... + log P(f28,28 | class)
After you compute the above decision function values for all ten classes for every test image, you will use them for MAP classification.
	"""
	answer=[]
	prior_data=NBC_trainer.priors(trained_data)
	for tups in trained_data: #does this get every tuple?
		numprob=[0,0,0,0,0,0,0,0,0,0,0]
		best_num=0
		best_prob=0
		for nums in range(10):
			for row in range(32):
				for col in range(32):
					if tups[0][row][col]==1:#pixel=1
						numprob[nums]=math.log1p(trained_data[nums][row][col])+numprob[nums]
					else :#pixel=0
						numprob[nums] = math.log1p(1-trained_data[nums][row][col]) + numprob[nums]
			numprob[nums]+=math.log1p(prior_data[nums])
			if numprob[nums] > best_prob:
				best_num = nums
				best_prob = numprob[nums]
			numprob[nums]=math.log(numprob[nums])
		numprob[10]=best_num
		answer.append(numprob)
	return answer
