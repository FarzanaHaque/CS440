import math
import numpy as np
import matplotlib.pyplot as plt

def display_odds_ratios(trained_data,confusion_matrix):
	used = set([])
	for i in range(4):
		highest = 0.0
		entry = (420,420)
		for row in range(10):
			for col in range(10):
				if confusion_matrix[row][col]>highest and row!=col and (row,col) not in used:
					highest = confusion_matrix[row][col]
					entry = (row,col)
		used.add(entry)
		odds_matrix = []
		for row in range(32):
			row_matrix = []
			for col in range(32):
				row_matrix.append(math.log((trained_data[entry[0]][row][col])/(trained_data
					[entry[1]][row][col])))
			odds_matrix.append(row_matrix)
		log_like1 = []
		for line in trained_data[entry[0]]:
			log_like1.append([math.log(x) for x in line])
		log_like2 = []
		for line in trained_data[entry[1]]:
			log_like2.append([math.log(x) for x in line])
		plt.imshow(np.array(log_like1),cmap='jet')
		plt.colorbar()
		plt.show()
		plt.imshow(np.array(log_like2),cmap='jet')
		plt.colorbar()
		plt.show()
		plt.imshow(np.array(odds_matrix),cmap='jet')
		plt.colorbar()
		plt.show()
	