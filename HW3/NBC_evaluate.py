import NBC_trainer as NBCt
import data_parsing as dp
import numpy as np

def evaluate(answers, test_data):
	"""
	Evals the answers that the NBC produces in testing
	:param answers: the 1d list answers from testing [(10 probs, answer),...]
	:param test_data: the parsed list of test_data from the parser
	:return: (list of classifcation accuracy for each digit (10 values),
			confusion matrix (10*10) (see webpage for details))
	"""
	# Calculate score
	amount_answer_class = np.array([0] * 10)
	amount_actual_class = np.array([0] * 10)
	amount_correct_class = np.array([0] * 10)

	for i in range(0, len(answers)):
		amount_answer_class[answers[i][10]] += 1
		amount_actual_class[test_data[i][dp.GET_ANSWER]] += 1
		if answers[i][10] == test_data[i][dp.GET_ANSWER]:
			amount_correct_class[answers[i][10]] += 1

	relative_error = np.absolute(amount_answer_class - amount_actual_class) / amount_actual_class
	class_acc = amount_correct_class / amount_actual_class

	# Calculate Confusion Matrix
	confusion_matrix = np.zeros((10,10))
	for i in range(0, len(answers)):

	return class_acc, None
