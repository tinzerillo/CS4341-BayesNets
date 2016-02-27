# node.py

from enum import Enum

class NodeStatus(Enum):
	TRUE = 't'
	FALSE = 'f'
	QUERY = 'q'
	RESOLVE = '-'

	def instForCharacter(character):
		if character == "t":
			return NodeStatus.TRUE
		elif character == "f":
			return NodeStatus.FALSE
		elif character == "?":
			return NodeStatus.QUERY
		elif character == "-":
			return NodeStatus.RESOLVE
		else:
			return NodeStatus.RESOLVE

class Node:
	def __init__(self, name, parents, probs, fileIndex):
		self._name = name
		self._parents = parents
		self._probs = probs

		self._fileIndex = fileIndex
		self._status = NodeStatus.RESOLVE


	@property
	def name(self):
		return self._name

	@property
	def status(self):
		return self._status

	@property
	def fileIndex(self):
	    return self._fileIndex
	
	
	def buildProbTable(self):
		for i in range(2**len(self._parents)+1):
			#print("binary", end="")
			for j in range(len(self._parents)):
				pass
				#print(self._parents[j])

	def binrepToProbIndex(self, binrep):
		#given 001, provide which index it is. Count up from 0 to start with

		for x in range(0,len(self._probs)):
			attempt = bin(x)
			if attempt == binrep:
				return x

		pass

	def probabilityForTrueParents(self, parentNames):

		positions = []
			#for example: node1, node2, node3
			#We need to figure out which positions those are in the parents list
		for x in range(0,len(self._parents)):
			if self._parents[x] in parentNames:
				positions.append(1)
			else:
				positions.append(0)

		#print("positions is:",positions)
		binaryString = ''.join(str(x) for x in positions)[::-1]
		#print("binaryString: ",binaryString)
		index = self.binrepToProbIndex(bin(int(binaryString, 2)))
		#print("binrepToProbIndex: ",index)
		#print("probability value:",self._probs[index])
		return self._probs[index]
				
		
	def __str__(self):
		return "name:" + str(self._name) + "\nparents: " + str(self._parents) + "\nprobs: " + str(self._probs) + "\n"