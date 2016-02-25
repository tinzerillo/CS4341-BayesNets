# bayes_nets.py

import networkx as nx
import sys
from node import * 

def parseInput(file):
	global G
	
	try:
		f = open(file, "r")
	except FileNotFoundError as e:
		print("Error: could not find", file)
		sys.exit(1)
	
	line = f.readline()

	counter = 0

	while line:
		n = line.find(':');
		name = line[0:n]
		
		line = line[n:]		
		b1 = line.find('[')
		b2 = line.find(']')
		
		nodes = list(line[b1+1:b2].split(" "))
		
		line = line[b2+1:]
		b3 = line.find('[')
		b4 = line.find(']')
		
		probs = list(line[b3+1:b4].split(" "))
		
		G.add_node(Node(name, nodes, probs, counter))
		
		line = f.readline()
		counter += 1
	
def findNode(grph, name):
	for node in grph.nodes():
		if node != "" and node._name == name:
			return node
	return ""
	
def findNodeFromIndex(grph, index):
	for node in grph.nodes():
		if node != "" and node._fileIndex == index:
			return node
	return ""

def parseQuery(grph, file):
	try:
		f = open(file, "r")
	except FileNotFoundError as e:
		print("Error: could not find", file)
		sys.exit(1)
	
	line = f.readline()

	chars = line.split(',')
	for x in range(len(chars)):
		node = findNodeFromIndex(G, x)

		node._status = NodeStatus.instForCharacter(chars[x])
			
G = nx.Graph()
parseInput(sys.argv[1])
for n in G.nodes():
	n.buildProbTable()
	print(n)
	pars = n._parents
	for p in pars:
		x = findNode(G, p)
		if x is not "":
			G.add_edge(x, n)

print(findNode(G, "node3").name)
findNode(G, "node5").probabilityForTrueParents(["node8", "node2"])
parseQuery(G, "query1.txt")

for n in G.nodes():
	print(n._status)
