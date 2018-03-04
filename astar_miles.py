import queue

miles_map = {"AB":1064,"AC":673,"AD":1401,"AE":277,"BC":958,"BD":1934,"BE":337,"CD":1001,"CE":399,"DE":387}

def miles_so_far(str):
	if len(str)==1:
		return 0
	mi = 0
	for i in range(0,len(str)-1):
		p = str[i:i+2]
		if p in miles_map:
			mi += miles_map[p]
		else:
			mi += miles_map[p[::-1]]
	return mi

def avg_miles_remaining(str,widgets):
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
		if tot > 0:
			rem += miles_so_far(s[-1]+w[ind:])
			
	return rem / len(widgets)

def h_g(str,widgets):
	return avg_miles_remaining(str,widgets)+miles_so_far(str)

def astar_miles(widgets):
	q = queue.PriorityQueue()
	q.put((h_g("A",widgets),"A"))
	q.put((h_g("B",widgets),"B"))
	q.put((h_g("D",widgets),"D"))
	visited = set(["A","B","D"])
	final=""
	min_mi = float('inf')
	while not q.empty():
		node = q.get()
		
		if node[0]>=min_mi:
			break
			
		if avg_miles_remaining(node[1],widgets)==0:
			if node[0] < min_mi:
				final=node[1]
				min_mi=node[0]
				continue
		
		if (node[1][-1]!="A") and (node[1]+"A") not in visited:
			q.put((h_g(node[1]+"A",widgets),node[1]+"A"))
			visited.add(node[1]+"A")
		
		if (node[1][-1]!="B") and (node[1]+"B") not in visited:
			q.put((h_g(node[1]+"B",widgets),node[1]+"B"))
			visited.add(node[1]+"B")
		
		if (node[1][-1]!="C") and (node[1]+"C") not in visited:
			q.put((h_g(node[1]+"C",widgets),node[1]+"C"))
			visited.add(node[1]+"C")
		
		if (node[1][-1]!="D") and (node[1]+"D") not in visited:
			q.put((h_g(node[1]+"D",widgets),node[1]+"D"))
			visited.add(node[1]+"D")
		
		if (node[1][-1]!="E") and (node[1]+"E") not in visited:
			q.put((h_g(node[1]+"E",widgets),node[1]+"E"))
			visited.add(node[1]+"E")
		
	return final
		
widg = ("AEDCA","BEACD","BABCE","DADBD","BECBD")
print(astar_miles(widg))	