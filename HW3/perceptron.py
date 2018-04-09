import numpy as np
import numpy.linalg as la
from random import shuffle
from sklearn.metrics import confusion_matrix

import data_parsing as parser
import copy

# 1- bias 0- no bias
# BIAS is amount of bias
BIAS_YES = 0
BIAS = 1

# number of epochs
EPOCHS = 4

# random weights
RANDOM_YES = 0

def img_to_vect(img):
	"""
	Converts a 32x32 img matrix to a 1025x1 vector.
	[0,0; 0,1; 0,2... 31,30; 31,31] (row *32 + col = idx)
	includes bias if enabled
	:param img: 32x32 np matrix
	:return: 1025x1 np vector
	"""
	vect = np.reshape(img, 1024)
	vect_list = list(vect)
	vect_list.append(BIAS_YES)
	vect = np.array(vect_list)
	return vect.reshape((1025, 1))


class Perceptron:
	training_data = None
	test_data = None
	weights = []

	train_per_epo = None
	test_score = None
	con_mat = None

	def __init__(self, training_data_fname, test_data_fname):
		"""
		Get my training data from a filename
		:param training_data_fname: the filename
		"""
		self.training_data = parser.create_data(training_data_fname)
		self.test_data = parser.create_data(test_data_fname)

	def build_weights(self):
		"""
		Arranged by class, ie index=0 is class=0.
		Currently set to 0s
		"""
		if RANDOM_YES == 1:
			self.weights = np.random.rand(10, 1025)
		else:
			self.weights = np.zeros((10, 1025))

		if BIAS_YES == 1:
			self.weights[:, 1024] = np.ones(10) * BIAS
		else:
			self.weights[:, 1024] = np.zeros(10)

	def train(self, learning_rate):
		"""
		Goes through all training data and trains the m_perceptron for 1 epoch
		:return: number of correct answers
		"""
		num_correct = 0
		t_data = self.training_data  # can randomize here
		wc = self.weights

		for tup in t_data:
			# Get Data
			img = tup[parser.GET_IMAGE]
			c = tup[parser.GET_ANSWER]
			# evaluate
			x = img_to_vect(img)
			decision_vect = wc @ x
			c_prime = np.argmax(decision_vect)
			# judge
			if c_prime == c:
				# correct
				num_correct += 1
				pass
			else:
				# incorrect, update
				wc[c, :] = wc[c, :] + learning_rate * x.T
				wc[c_prime, :] = wc[c_prime, :] - learning_rate * x.T

		self.weights = wc
		return num_correct

	def iterative_train(self, epochs):
		"""
		Runs the train function epochs times and returns its accuracy
		against the training set for each epoch
		:return: list of accuracies matching epoch by position
		"""
		learning_rate = 1.0 / 1.0
		num_correct_epo = []

		# train
		for i in range(0, epochs):
			ret = self.train(learning_rate)
			num_correct_epo.append(ret)
			learning_rate = ((learning_rate ** -1) + 1) ** -1  # CHANGE LEARNING RATE HERE

		# training results
		num_correct_epo = np.array(num_correct_epo)
		percentage_epo = num_correct_epo / len(self.training_data)
		return percentage_epo

	def test(self):
		"""
		Tests the trained m_perceptron against the test data
		:return: score as percentage, 10*10 matrix as percentage confusion matrix
		"""
		num_correct = 0
		t_data = self.test_data
		wc = self.weights

		ret_ans = []
		actual = []

		# test
		for tup in t_data:
			# Get Data
			img = tup[parser.GET_IMAGE]
			c = tup[parser.GET_ANSWER]
			# evaluate
			x = img_to_vect(img)
			decision_vect = wc @ x
			c_prime = np.argmax(decision_vect)
			# mark answers
			ret_ans.append(c_prime)
			actual.append(c)
			# judge
			if c_prime == c:
				# correct
				num_correct += 1
				pass

		# Handle Confusion Matrix
		score = np.array(num_correct) / len(self.test_data)
		con_mat = confusion_matrix(actual, ret_ans)
		con_mat_per = con_mat/con_mat.sum(axis=1)[:, None]

		return score, con_mat

	def report(self):
		"""
		Prints out results of training and testing
		:return: None
		"""
		print("Accuracy on the Training Data per Epoch:")
		print(self.train_per_epo)
		print("")
		print("Test Accuracy: " + str(self.test_score))
		print("Confusion Matrix as Percentages: ")
		print(self.con_mat)

	def do_everything(self):
		"""
		Trains and tests the m_perceptron and then reports the data
		:return:
		"""
		self.build_weights()
		self.train_per_epo = self.iterative_train(EPOCHS)
		self.test_score, self.con_mat = self.test()
		self.report()


def main():
	np.set_printoptions(linewidth=1000)
	classifier = Perceptron('optdigits-orig_train.txt', 'optdigits-orig_test.txt')
	classifier.do_everything()
	pass


if __name__ == "__main__":
	main()