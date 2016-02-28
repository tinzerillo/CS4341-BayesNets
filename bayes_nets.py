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

def generateSample(grph):

	toposorted = nx.topological_sort(grph)
	sample = {}

	for node in toposorted:

		trueParents = []

		if '' not in node._parents:
			for node_parent in node._parents:
				#lookup in the sample what the probability is
				node_parent_status = sample[node_parent]
				if node_parent_status == NodeStatus.TRUE:
					trueParents.append(node_parent)

		value = node.probabilityForTrueParents(trueParents)

		#Now we have a probability value

		x = random.random()

		if x < float(value):
			sample[node._name] = NodeStatus.TRUE
		else:
			sample[node._name] = NodeStatus.FALSE

	return sample

def generateWeightedSample(grph):

	toposorted = nx.topological_sort(grph)
	sample = {}

	for node in toposorted:
	
		weight = 1.0

		trueParents = []

		if '' not in node._parents:
			for node_parent in node._parents:
				#lookup in the sample what the probability is
				node_parent_status = sample[node_parent]
				if node_parent_status ==  NodeStatus.TRUE:
					trueParents.append(node_parent)

		value = node.probabilityForTrueParents(trueParents)

		#Now we have a probability value

		#If it's evidence
		if (node._status == NodeStatus.TRUE or node._status == NodeStatus.FALSE):
			sample[node._name] = node._status
			weight = weight * float(value)
		else:
			x = random.random()

			if x < float(value):
				sample[node._name] = NodeStatus.TRUE
			else:
				sample[node._name] = NodeStatus.FALSE


	return (sample, weight)

def likelihoodSampling(grph, N, query_node):

	samples_true = 0

	for x in range(0,N):
		sample, weight = generateWeightedSample(grph)

		if sample[query_node._name] is NodeStatus.TRUE:
			samples_true += weight

	return round(samples_true/N, 3)
	
def parseQuery(grph, file):
	try:
		f = open(file, "r")
	except FileNotFoundError as e:
		print("Error: could not find", file)
		sys.exit(1)
	
	line = f.readline()

	query_node = None

	chars = line.split(',')
	for x in range(len(chars)):
		node = findNodeFromIndex(G, x)
		node._status = NodeStatus.instForCharacter(chars[x])
		if node._status is NodeStatus.QUERY:
			query_node = node

	return query_node

def compareSampleToGraph(graph, sample):
	for n in list(sample):
		node = findNode(graph, n)
		if node._status == NodeStatus.TRUE:
			if sample[n] == NodeStatus.FALSE:
				return False
		elif node._status == NodeStatus.FALSE:
			if sample[n] == NodeStatus.TRUE:
				return False
	return True

def rejectionSample(grph, N, query_node):
	queryTrue = 0
	sampleNotDiscarded = 0

	for x in range(0, N):
		sample = generateSample(grph)
		if compareSampleToGraph(grph, sample) is True:
			sampleNotDiscarded += 1
			if sample[query_node._name] is NodeStatus.TRUE:
				queryTrue += 1
				
	return round(queryTrue/sampleNotDiscarded, 3)


G = nx.DiGraph()
parseInput(sys.argv[1])
for n in G.nodes():
	n.buildProbTable()
	pars = n._parents
	for p in pars:
		x = findNode(G, p)
		if x is not "":
			G.add_edge(x, n)


query_node = parseQuery(G, "query2.txt")

print("TOPOSORT:")
sorted = nx.topological_sort(G)
for node in sorted:
	#print("["+node.name+"]",node._status)
	pass
	
print("SAMPLE:")
#print(generateSample(G))
print(rejectionSample(G, 99000, query_node))
print(likelihoodSampling(G, 10000, query_node))
