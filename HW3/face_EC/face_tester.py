"""
Tester function matching 1.1 testing
"""
import math
import NBC_trainer

#def fpriors(data):



def test(training_data,trained_data, test_data):
	"""
	Classifies all the data given the trained_data from training.
	:param trained_data: the 3d list returned from training. See training for exact specs
	:param test_data: the data to test the trained NBC against
	:return: 1d array matching the data from data_parser
	log P(class) + log P(f1,1 | class) + log P(f1,2 | class) + ... + log P(f28,28 | class)
After you compute the above decision function values for all ten classes for every test image, you will use them for MAP classification.
	"""
	answer=[]
	prior_data=NBC_trainer.priors(training_data)
	for tups in test_data: #get each tuple in parsed test data
		numprob=[0.0,0.0,0.0,] #inital probs of each num class
		best_num=-1
		best_prob=-9999999
		for nums in range(2):
			numprob[nums]=math.log(prior_data[nums])
			for row in range(70):
				for col in range(60):
					if tups[0][row][col]=="#":#pixel=1
						numprob[nums]+=math.log(trained_data[nums][row][col])
					else :#pixel=" "
						numprob[nums] += math.log(1-trained_data[nums][row][col])
			if numprob[nums] >= best_prob:
				best_num = nums
				best_prob = numprob[nums]
			numprob[nums]=math.exp(numprob[nums])
		numprob[2]=best_num
		answer.append(numprob)
	return answer
