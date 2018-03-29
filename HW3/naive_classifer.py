"""
This part for 1.1, Naive Bayesian Classifier.
"""
import data_parsing as parser


class NBC:
	"""
	Naive Bayesian Classifier (NBC)
	"""
	t_data = None

	def __init__(self, training_data_fname):
		"""
		Get my training data from a filename
		:param training_data_fname:
		"""
		self.t_data = parser.create_data(training_data_fname)


def main():
	classifier = NBC('optdigits-orig_train.txt')
	parser.print_image(classifier.t_data[0][parser.GET_IMAGE])
	pass


if __name__ == "__main__":
	main()
