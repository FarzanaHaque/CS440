"""
This part for 1.1, Naive Bayesian Classifier.
"""
import data_parsing as parser
import NBC_trainer
import NBC_tester
import NBC_evaluate
import NBC_odds_ratio


class NBC:
	"""
	Naive Bayesian Classifier (NBC)
	"""
	training_data = None
	test_data = None

	trained_data = None
	answers = None

	class_acc = None
	confusion_matrix = None

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
		:param training_data: the data from data parsing
		:return: 3D list of probabilites of each pixel of each class. 1- class, 2- y, row, 3- x, column
		"""
		self.trained_data = NBC_trainer.train(training_data)
		pass

	def testing(self, trained_data, test_data):
		"""
		Classifies all the data given the trained_data from training.
		:param trained_data: the 3d list returned from training. See training for exact specs
		:param test_data: the data to test the trained NBC against
		:return: 1d array matching the data from data_parser [(10 probs, answer),...]
		"""
		self.answers = NBC_tester.test(trained_data, test_data)
		pass

	def evaluate(self, answers, test_data):
		"""
		Evals the answers that the NBC produces in testing
		:param answers: the 1d list answers from testing [(10 probs, answer),...]
		:param test_data: the parsed list of test_data from the parser
		:return: (list of classifcation accuracy for each digit (10 values),
				confusion matrix (10*10) (see webpage for details))
		"""
		self.class_acc, self.confusion_matrix = NBC_evaluate.evaluate(answers, test_data)

	def calculate_odds_ratio(self, trained_data, confusion_matrix):
		"""
		Displays the odds ratio given a 3d set of trained data
		:param trained_data: the 3d array of trained data
		:return: None
		"""
		NBC_odds_ratio.calculate_odds_ratio(trained_data)


def main():
	classifier = NBC('optdigits-orig_train.txt', 'optdigits-orig_test.txt')
	parser.print_image(classifier.test_data[0][parser.GET_IMAGE])
	pass


if __name__ == "__main__":
	main()
