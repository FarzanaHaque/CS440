"""
This module handles parsing in test data.
"""

GET_IMAGE = 0
GET_ANSWER = 1


def create_data(filename):
	"""
	Generates a list of training data in a list of tuples [(data in a 2d list, true result), ...]
	:param filename: name of file to input
	:return: data in a list of tuples [(data in a 2d list of ints, true result in int), ...]
	"""
	file = open(filename, "r")
	data = []
	current_image = []
	for line in file:
		if len(line) != 32 + 1:  # remember the \n at the end
			# found the end of the number
			answer = int(line)
			in_data = (current_image, answer)
			data.append(in_data)
			current_image = []
		else:
			newline = []
			for c in line:
				if c != '\n':
					newline.append(int(c))
			current_image.append(newline)
	file.close()
	return data


def print_image(img):
	"""
	Prints out the 2d array of ints in the character array in a nice format
	:param img: 2d array of integers (image)
	:return: None
	"""
	for line in img:
		for c in line:
			print(c, end="")
		print()


def main():
	data = create_data('optdigits-orig_train.txt')
	print_image(data[-1][GET_IMAGE])
	pass


if __name__ == "__main__":
	main()
