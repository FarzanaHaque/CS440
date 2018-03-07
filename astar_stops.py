import queue
import random

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
	#return len(str)    #Dijkstra's Algorithm

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
		
		if (node[1][-1]!="A") and (node[1]+"A") not in visited:
			q.put((h_g(node[1]+"A",widgets),node[1]+"A"))
			visited.add(node[1]+"A")
		
		if (node[1][-1]!="B") and (node[1]+"B") not in visited:
			q.put((h_g(node[1]+"B",widgets),node[1]+"B"))
			visited.add(node[1]+"B")
		
		if (node[1][-1]!="C")and(node[1]+"C") not in visited:
			q.put((h_g(node[1]+"C",widgets),node[1]+"C"))
			visited.add(node[1]+"C")
		
		if (node[1][-1]!="D")and(node[1]+"D") not in visited:
			q.put((h_g(node[1]+"D",widgets),node[1]+"D"))
			visited.add(node[1]+"D")
		
		if (node[1][-1]!="E")and(node[1]+"E") not in visited:
			q.put((h_g(node[1]+"E",widgets),node[1]+"E"))
			visited.add(node[1]+"E")
	
	print("nodes expanded %d" % len(visited))
	return final
		
#widg = ("AEDCA","BEACD","BABCE","DADBD","BECBD")
#sol = astar_stops(widg)
#print(sol)	
#print(len(sol))	

def int_to_char(i):
	if i==0:
		return "A"
	elif i==1:
		return "B"
	elif i==2:
		return "C"
	elif i==3:
		return "D"
	return "E"

def generate_widg(n):
	widg = []
	for i in range(0,5):
		chars = []
		for j in range(0,n):
			r = random.randint(0,4)
			c = int_to_char(r)
			while j>0 and c==chars[j-1]:
				r = random.randint(0,4)
				c = int_to_char(r)
			chars.append(c)
		widg.append(chars)
	return (''.join(widg[0]),''.join(widg[1]),''.join(widg[2]),''.join(widg[3]),''.join(widg[4]))
	
widg = generate_widg(8)
sol = astar_stops(widg)
print(sol)
print(len(sol))