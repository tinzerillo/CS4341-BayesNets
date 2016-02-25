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
		
		G.add_node(Node(name, nodes, probs))
		
		line = f.readline()
	
def findNode(grph, name):
	for node in grph.nodes():
		if node != "" and node._name == name:
			return node
	return ""
	
def parseQuery(grph, file):
	pass

G=nx.Graph()
parseInput(sys.argv[1])
for n in G.nodes():
	n.buildProbTable()
	pars = n._parents
	for p in pars:
		x = findNode(G, p)
		if x is not "":
			G.add_edge(x, n)
			
