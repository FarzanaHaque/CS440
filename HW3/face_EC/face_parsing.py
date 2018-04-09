"""
This module handles parsing in test data.
"""

GET_IMAGE = 0
GET_ANSWER = 1


def create_data(datafile,labelfile):
	"""
	Generates a list of training data in a list of tuples [(data in a 2d list, true result), ...]
	:param filename: name of file to input
	:return: data in a list of tuples [(data in a 2d list of ints, true result in int), ...]
	"""
	file = open(labelfile, "r")
	labels=[]
	for line in file:
		for c in line:
			if c!='\n':
				labels.append(int(c))
	file.close()
	#print(len(labels))
	file=open(datafile,"r")
	data = []
	current_image = []
	line_count=0
	for line in file:
		newline=[]
		for c in line:
			if c != '\n':
				newline.append(c)
			current_image.append(newline)
		line_count+=1
		if(line_count%70==0):#maybe off by one
			answer=labels[line_count//70-1]
			in_data=(current_image,answer)
			#in_data.append(labels[line_count])
			data.append(in_data)
			current_image=[]

	"""
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
		current_image.append(newline)"""
	file.close()
	print(len(labels))
	print(len(data))
	return data


def print_image(img):
	"""
	Prints out the 2d array of ints in the character array in a nice format
	:param img: 2d array of integers (image)
	:return: None
	"""
	for line in img:
		#for c in line:
		#	print(c)
		print(line)
		print()


def main():
	data = create_data('facedata/facedatatrain','facedata/facedatatrainlabels')
	for i in range(20):
		print_image(data[i][GET_IMAGE])
	#print(len(data[0])) #61*70
	pass


if __name__ == "__main__":
	main()
