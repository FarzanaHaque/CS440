import face_trainer as NBCt
import face_parsing as dp
import numpy as np


def get_best_and_worst(answers, test_data, in_class):
	"""
	finds the tokens that have the highest probability and lowest probability
	:param answers:
	:param test_data:
	:param in_class: the class
	:return: [(2d img, best prob), (2d img, worst prob)]
	"""
	ret = [[None, 0.0], [None, 1.0]]
	for i in range(0, len(answers)):
		if test_data[i][dp.GET_ANSWER] == in_class:
			if answers[i][in_class] > ret[0][1]:
				# found maxer
				ret[0][1] = answers[i][in_class]
				ret[0][0] = test_data[i][dp.GET_IMAGE]
			elif answers[i][in_class] < ret[1][1]:
				# found miner
				ret[1][1] = answers[i][in_class]
				ret[1][0] = test_data[i][dp.GET_IMAGE]
	return ret


def print_best_and_worst(best_and_worst, in_class):
	print("For class: " + str(in_class))
	print("Highest Prob of " + str(best_and_worst[0][1]) + " | Image Below:")
	dp.print_image(best_and_worst[0][0])
	print("Lowest Prob of " + str(best_and_worst[1][1]) + " | Image Below:")
	dp.print_image(best_and_worst[1][0])
	print("")


def evaluate(answers, test_data):
	"""
	Evals the answers that the NBC produces in testing
	:param answers: the 1d list answers from testing [(2 probs, answer),...]
	:param test_data: the parsed list of test_data from the parser
	:return: (list of classifcation accuracy for each digit (2 values),
			confusion matrix (2*2) (see webpage for details))
	"""
	# Calculate score
	amount_answer_class = np.array([0] * 2)
	amount_actual_class = np.array([0] * 2)
	amount_correct_class = np.array([0] * 2)

	for i in range(0, len(answers)):
		amount_answer_class[answers[i][2]] += 1
		amount_actual_class[test_data[i][dp.GET_ANSWER]] += 1
		if answers[i][2] == test_data[i][dp.GET_ANSWER]:
			amount_correct_class[answers[i][2]] += 1

	relative_error = np.absolute(amount_answer_class - amount_actual_class) / amount_actual_class
	class_acc = amount_correct_class / amount_actual_class

	# Calculate Confusion Matrix
	confusion_matrix = np.zeros((2, 2))
	for i in range(0, len(answers)):
		confusion_matrix[test_data[i][dp.GET_ANSWER]][answers[i][2]] += 1

	for i in range(0, 2):
		confusion_matrix[i, :] = confusion_matrix[i, :] / amount_actual_class[i]

	# Print the most and least fit stuff for each image
	print("The best and worst of each class. Which images had the highest and lowest prob?")
	best_and_worst_tokens = []
	for i in range(0, 2):
		temp = get_best_and_worst(answers, test_data, i)
		print_best_and_worst(temp, i)
		best_and_worst_tokens.append(temp)

	print("From Evaluate: Accuracy List. Each percentage matches to the class by position")
	print(class_acc)
	print("From Evaluate: Average accuracy. Average of acc list")
	print(np.average(class_acc))
	print("From Evaluate: Confusion Matrix. See online for exact definition. Notice that the diagonals match the acc list")
	print(confusion_matrix)
	return class_acc, confusion_matrix
