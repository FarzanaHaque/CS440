import numpy as np
from sklearn.metrics import confusion_matrix
from sklearn import tree

import data_parsing as parser


def img_to_vect(img):
	"""
	Converts a 32x32 img matrix to a 1025x1 vector.
	[0,0; 0,1; 0,2... 31,30; 31,31] (row *32 + col = idx)
	includes bias if enabled
	:param img: 32x32 np matrix
	:return: 1025x1 np vector
	"""
	vect = np.reshape(img, 1024)
	return vect


training_data = parser.create_data('optdigits-orig_train.txt')
test_data = parser.create_data('optdigits-orig_test.txt')

training_imgs = [img_to_vect(i[0]) for i in training_data]
training_ans = [i[1] for i in training_data]

clf = tree.DecisionTreeClassifier()
clf = clf.fit(training_imgs, training_ans)

test_imgs = [img_to_vect(i[0]) for i in test_data]
test_ans = [i[1] for i in test_data]

guesses = clf.predict(test_imgs)
con_mat = confusion_matrix(test_ans, guesses)
con_mat_per = con_mat/con_mat.sum(axis=1)[:, None]

correct_count = 0
for i in range(0, len(test_ans)):
	if guesses[i] == test_ans[i]:
		correct_count += 1

print(correct_count / len(test_ans))

print(con_mat)
print(np.diag(con_mat_per))
