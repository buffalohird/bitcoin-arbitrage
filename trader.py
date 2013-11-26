import time
from currency import currency
import random
import Queue
from copy import copy

class trader:

 def __init__(self, api, chain, expectedProfit):
  self.maxGamma = 5
  self.api = api
  self.chain = copy(chain)
  self.expectedProfit = expectedProfit

 def executeChain(self, chain, startQuantity):
 	if len(chain) <= 1:
 		return startQuantity
 	type1 = chain.pop(0)
 	
 	print "type1 and type2:", type1, chain[0]
 	newQuantity = startQuantity * self.executeTrade(type1, chain[0], startQuantity)
 	#newQuantity = self.executeTrade(type1, chain[0], startQuantity)
 	return self.executeChain(chain, newQuantity)

 def executeTrade(self, type1, type2, quantity):
 	#return self.api.makeTrade(type1, type2, quantity)
 	return self.api.getTrade(type1, type2)
