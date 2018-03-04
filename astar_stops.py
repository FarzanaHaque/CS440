import queue

def avg_letters_remaining(str,widgets):
	rem=0
	for w in widgets:
		tot=len(w)
		ind=0
		for s in str:
			if tot==0:
				break
			if w[ind]==s:
				tot-=1
				ind+=1
		rem+=tot
	return rem / len(widgets)

def h_g(str,widgets):
	return avg_letters_remaining(str,widgets)+len(str)

def astar_stops(widgets):
	q = queue.PriorityQueue()
	q.put((h_g("A",widgets),"A"))
	q.put((h_g("B",widgets),"B"))
	q.put((h_g("D",widgets),"D"))
	visited = set(["A","B","D"])
	final=""
	min_len = float('inf')
	while not q.empty():
		node = q.get()
		
		if node[0]>=min_len:
			break
			
		if avg_letters_remaining(node[1],widgets)==0:
			if node[0] < min_len:
				final=node[1]
				min_len=node[0]
				continue
		
		if (node[1]+"A") not in visited:
			q.put((h_g(node[1]+"A",widgets),node[1]+"A"))
			visited.add(node[1]+"A")
		
		if (node[1]+"B") not in visited:
			q.put((h_g(node[1]+"B",widgets),node[1]+"B"))
			visited.add(node[1]+"B")
		
		if (node[1]+"C") not in visited:
			q.put((h_g(node[1]+"C",widgets),node[1]+"C"))
			visited.add(node[1]+"C")
		
		if (node[1]+"D") not in visited:
			q.put((h_g(node[1]+"D",widgets),node[1]+"D"))
			visited.add(node[1]+"D")
		
		if (node[1]+"E") not in visited:
			q.put((h_g(node[1]+"E",widgets),node[1]+"E"))
			visited.add(node[1]+"E")
		
	return final
		
widg = ("AEDCA","BEACD","BABCE","DADBD","BECBD")
print(astar_stops(widg))	
		