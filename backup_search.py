import time
from currency import currency
import random
import Queue
from copy import copy


class search:

 def __init__(self, api):
 	self.api = api
 	self.name = "search"
 	self.gamma = 0.9

 def nullHeuristic(state, problem=None):
  """
  A heuristic function estimates the cost from the current state to the nearest
  goal in the provided SearchProblem.  This heuristic is trivial.
  """
  return 0	

 def makeSearch(self, root):
  "Search the node that has the lowest combined cost and heuristic first."
  fringe = []

  # 
  node = [root, [root.value.name], 1.0]
  maxPath = [root, [root.value.name], 0.0]
  while node:
  	children = node[0].getChildren()
  	if children == []:
  		#print "NOOOOO"
  		#print "final: calling getTrade %s %s" % (str(node[0].value.name), str(root.value.name))
  		newNode = [tree(root.value), node[1] + [root.value.name], node[2] * self.api.getTrade(node[0].value.name, root.value.name)]
  		print "Final expanded node: ", newNode[1]
  		self.formatTreeSolution(newNode)
  		#print "old number: ", node[2]
  		#print "new number: ", newNode[2]
  		if newNode[2] > maxPath[2]:
  			maxPath = newNode

  	for child in children:
  		#print '\n'
  		#print self.api.getTrade(node[0].value.name, child.value.name)
  		#print '\n'
  		#print node, str(node[0])
  		#print node[0].value.name
  		#print child.value.name
  		#print '\n\n\n'
  		#print "routine: calling getTrade %s %s" % (str(node[0].value.name), str(child.value.name))
  		newNode = [child, node[1] + [child.value.name],  node[2] * self.api.getTrade(node[0].value.name, child.value.name)]
  		print "Final expanded node: ", newNode[1]
  		#print "old number: ", node[2]
  		#print "new number: ", newNode[2]
  		#time.sleep(0)
  		fringe.append(newNode)
  	if not fringe:
  		return maxPath
  	node = fringe.pop()

  return maxPath[1]

 def expand(self, initial, node):
 	#should never happen
 	#if node.name == initial.name
 		#return None

 	newChildren = []
 	for successor in node.value.successors:
 		if successor == initial.value.name:
 			continue
 		newSuccessor = currency(successor)
 		#print "%s : %s" % (newSuccessor.name, newSuccessor.successors)
 		newNode = tree(newSuccessor)
 		newNode.gamma = node.gamma * self.gamma
 		newChildren.append(newNode)
 		
 		value = random.random()
 		if(value < newNode.gamma):
 			self.expand(initial, newNode)

 	node.children = newChildren


 def createTree(self, initial):
 	root = tree(initial)
 	self.expand(root, root)
 	#print root
 	return root

 def createAllTrees(self, currencies):
 	trees = []
 	for currency in currencies:
 		newTree = self.createTree(currency)
 		trees.append(newTree)

 	return trees


 def solveTree(self, tree):
 	returnValue = self.makeSearch(tree)
 	returnString = self.formatTreeSolution(returnValue)
 	return returnValue

 def findBestTree(self, trees):

 	solutions = []
 	for tree in trees:
 		newSolution = self.makeSearch(tree)
 		solutions.append(newSolution)

 	bestSolution =  max(solution[2] for solution in solutions)
 	return bestSolution


 def formatTreeSolution(self, solution):
	returnString = "\n Solution found at node %s \n Solution path: %s \n Solution profit (percent): %s \n" % (solution[0], solution[1], solution[2])
 	print returnString
 	return returnString


class tree:
 def __init__(self, value):
 	self.children = []
 	self.value = value
 	self.gamma = 1.0

 def __str__(self):
 	returnString = "("
 	returnString += str(self.value) + "): \n   ["
 	for item in self.children:
 		returnString += str(item)
 	returnString += "]"
 	return returnString

 def getChildren(self):
 	return self.children

 def addChild(self, child):
 	self.children.append(child)
