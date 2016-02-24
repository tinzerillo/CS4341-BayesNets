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
		if len(nodes) is 0:
			node1 = None
			node2 = None
		elif len(nodes) is 1:
			node1 = nodes[0]
			node2 = None
		elif len(nodes) is 2:
			node1 = nodes[0]
			node2 = nodes[1]
		else:
			print("ERROR")
		
		line = line[b2+1:]
		b3 = line.find('[')
		b4 = line.find(']')
		
		probs = list(line[b3+1:b4].split(" "))
		
		G.add_node(Node(name, node1, node2, probs))
		
		line = f.readline()
		

G=nx.Graph()
parseInput(sys.argv[1])
for n in G.nodes():
	n.toString()