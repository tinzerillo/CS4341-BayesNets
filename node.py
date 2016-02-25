# node.py
	
class Node:
	def __init__(self, name, parents, probs):
		self._name = name
		self._parents = parents
		self._probs = probs
	
	@property
	def name(self):
		return self._name
	
	def buildProbTable(self):
		for i in range(2**len(self._parents)+1):
			print("binary", end="")
			for j in range(len(self._parents)):
				print(self._parents[j])
				
		
	def toString(self):
		print("name:", self._name, "\nparents:", self._parents, "\nprobs", self.probs, "\n")