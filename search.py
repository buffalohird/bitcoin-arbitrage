import time
from currency import currency
import random
import Queue
from copy import copy


class search:

 def __init__(self, api):
  self.maxGamma = 5
  self.api = api
  self.name = "search"
  self.gamma = 1


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
    if node[0].value.name == root.value.name:
      #self.formatTreeSolution(node)
      #print node[1]
      if node[2] > maxPath[2] and len(node[1]) > 3:
        maxPath = node

    for child in children:
      newNode = [child, node[1] + [child.value.name], node[2] * self.api.getTrade(node[0].value.name, child.value.name)]
      #print "expanded node: ", newNode[1]
      fringe.append(newNode)
    if not fringe:
      return maxPath
    node = fringe.pop()

  return maxPath[1]



 def expand(self, initial, node):
 	#should never happen
 	#if node.name == initial.name
 		#return None

  if node.gamma == self.maxGamma:
    node.children = []
    return

  newChildren = []
  for successor in node.value.successors:
    newSuccessor = currency(successor)
    newNode = tree(newSuccessor)
    newNode.gamma = node.gamma + self.gamma
    newChildren.append(newNode)

    self.expand(initial, newNode)

    #value = random.random()
    #if(value < newNode.gamma):
      #self.expand(initial, newNode)

  node.children = newChildren

 def createTree(self, initial):
 	root = tree(initial)
 	self.expand(root, root)
 	return root

 def createAllTrees(self, currencies):
 	trees = []
 	for currency in currencies:
 		newTree = self.createTree(currency)
 		trees.append(newTree)

 	return trees


 def solveTree(self, tree):
 	returnValue = self.makeSearch(tree)
 	return returnValue

 def solveAllTrees(self, trees):
  solutions = []
  for tree in trees:
    newSolution = self.makeSearch(tree)
    solutions.append(newSolution)

  bestSolution = max(solutions, key=lambda p: max(p[2:]))
  return bestSolution


 def formatTreeSolution(self, solution):
	returnString = "\n Solution found at node %s \n Solution path: %s \n Solution profit (percent): %s \n" % (solution[0], solution[1], solution[2])
 	print returnString
 	return returnString

 def findSolution(self, initial):
  searchTree = self.createTree(initial)
  solvedSearchTree = self.solveTree(searchTree)
  self.formatTreeSolution(solvedSearchTree)
  return solvedSearchTree

 def findBestSolution(self, currencies):
  trees = self.createAllTrees(currencies)
  bestSolution = self.solveAllTrees(trees)
  self.formatTreeSolution(bestSolution)
  return bestSolution


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
