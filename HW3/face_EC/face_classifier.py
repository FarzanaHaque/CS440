"""
This part for 1.1, Naive Bayesian Classifier.
"""
import face_parsing as parser
import face_trainer
import face_tester
import FNBC_evaluate
import FNBC_odds_ratio


class FNBC:
	"""
	Naive Bayesian Classifier (NBC)
	"""
	training_data = None
	test_data = None

	trained_data = None
	answers = None

	class_acc = None
	confusion_matrix = None

	def __init__(self, training_data_fname,train_label, test_data_fname, test_label):
		"""
		Get my training data from a filename
		:param training_data_fname: the filename
		"""
		self.training_data = parser.create_data(training_data_fname,train_label)
		self.test_data = parser.create_data(test_data_fname,test_label)

	def training(self, training_data):
		"""
		Trains the data and returns a 3D array (a list of matrices) of probabilites of each pixel in each class
		Think a heatmap of each class as a matrix
		:param training_data: the data from data parsing
		:return: 3D list of probabilites of each pixel of each class. 1- class, 2- y, row, 3- x, column
		"""
		self.trained_data = face_trainer.train(training_data)
		pass

	def testing(self, training_data, trained_data, test_data):
		"""
		Classifies all the data given the trained_data from training.
		:param trained_data: the 3d list returned from training. See training for exact specs
		:param test_data: the data to test the trained NBC against
		:return: 1d array matching the data from data_parser [(10 probs, answer),...]
		"""
		self.answers = face_tester.test(training_data, trained_data, test_data)
		pass

	def evaluate(self, answers, test_data):
		"""
		Evals the answers that the NBC produces in testing
		:param answers: the 1d list answers from testing [(10 probs, answer),...]
		:param test_data: the parsed list of test_data from the parser
		:return: (list of classifcation accuracy for each digit (10 values),
				confusion matrix (10*10) (see webpage for details))
		"""
		self.class_acc, self.confusion_matrix = FNBC_evaluate.evaluate(answers, test_data)

	#def display_odds_ratios(self, trained_data, confusion_matrix):
		"""
		Displays the odds ratio given a 3d set of trained data
		:param trained_data: the 3d array of trained data
		:return: None
		"""
	#	FNBC_odds_ratio.display_odds_ratios(trained_data, confusion_matrix)

	def do_everything(self):
		self.training(self.training_data)
		#print(self.trained_data)
		self.testing(self.training_data, self.trained_data, self.test_data)
		#for i in range(10):
		#    print(str(i+1+9)+":"+str(self.answers[i+9][2]))
		self.evaluate(self.answers, self.test_data)
		#self.display_odds_ratios(self.trained_data, self.confusion_matrix)

def main():
	classifier = FNBC('facedata/facedatatrain','facedata/facedatatrainlabels','facedata/facedatatest','facedata/facedatatestlabels')
	classifier.do_everything()
	#print(classifier.training_data)
	pass


if __name__ == "__main__":
	main()
