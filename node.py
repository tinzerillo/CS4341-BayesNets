# node.py
	
class Node:
	def __init__(self, name, parent1, parent2, probs):
		self.name = name
		self.parent1 = parent1
		self.parent2 = parent2
		self.probs = probs
		
	def toString(self):
		print("name:", self.name, "\nparent1:", self.parent1, "parent2:", self.parent2, "\nprobs", self.probs, "\n")