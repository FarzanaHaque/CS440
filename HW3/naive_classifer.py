"""
This part for 1.1, Naive Bayesian Classifier.
"""
import data_parsing as parser
import NBC_trainer
import NBC_tester


class NBC:
	"""
	Naive Bayesian Classifier (NBC)
	"""
	training_data = None
	test_data = None

	trained_data = None
	answers = None

	def __init__(self, training_data_fname, test_data_fname):
		"""
		Get my training data from a filename
		:param training_data_fname: the filename
		"""
		self.training_data = parser.create_data(training_data_fname)
		self.test_data = parser.create_data(test_data_fname)

	def training(self, training_data):
		"""
		Trains the data and returns a 3D array (a list of matrices) of probabilites of each pixel in each class
		Think a heatmap of each class as a matrix
		:param data: the data from data parsing
		:return: 3D list of probabilites of each pixel of each class. 1- class, 2- y, row, 3- x, column
		"""
		self.trained_data = NBC_trainer.train(training_data)
		pass

	def testing(self, trained_data, test_data):
		"""
		Classifies all the data given the trained_data from training.
		:param trained_data: the 3d list returned from training. See training for exact specs
		:return: 1d array matching the data from data_parser
		"""
		self.answers = NBC_tester.test(trained_data, test_data)
		pass




def main():
	classifier = NBC('optdigits-orig_train.txt')
	parser.print_image(classifier.data[0][parser.GET_IMAGE])
	pass


if __name__ == "__main__":
	main()
