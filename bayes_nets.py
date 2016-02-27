# bayes_nets.py

import networkx as nx
import sys
import random
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

# n = num samples to generate
def generateSample(grph):

	toposorted = nx.topological_sort(grph)
	sample = {}

	for node in toposorted:

		print("Operating on node",node._name)

		trueParents = []

		if '' not in node._parents:
			for node_parent in node._parents:
				#lookup in the sample what the probability is
				node_parent_status = sample[node_parent]
				if node_parent_status == 'T':
					trueParents.append(node_parent)

		print("trueParents is",trueParents)

		value = node.probabilityForTrueParents(trueParents)

		#Now we have a probability value

		x = random.random()

		if x < float(value):
			sample[node._name] = 'T'
		else:
			sample[node._name] = 'F'

	return sample
	
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

G = nx.DiGraph()
parseInput(sys.argv[1])
for n in G.nodes():
	n.buildProbTable()
	pars = n._parents
	for p in pars:
		x = findNode(G, p)
		if x is not "":
			G.add_edge(x, n)


parseQuery(G, "query1.txt")

print("TOPOSORT:")
sorted = nx.topological_sort(G)
for node in sorted:
	print("["+node.name+"]",node._status)
	pass
	
print("SAMPLE:")
print(generateSample(G))
