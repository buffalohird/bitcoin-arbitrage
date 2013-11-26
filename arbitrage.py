import httplib
import urllib
import json
import hashlib
import hmac
import time
from currency import currency
from search import search
from trader import trader
from user import user
from logger import logger
from api import api
from copy import copy
from datetime import datetime
import threading
import random
import sys
import atexit

class arbitrage:


 def __init__(self):
   self.api = None
   self.logger = None
   self.user = None
   self.setCurrencies(1)

 def start(self):
  print "a) get api"
  self.startApi()
  print "b) initiate logger"
  self.startLogger()
  print "c) get user"
  self.startUser()

  atexit.register(self.logger.writeFile, 'new.csv')

 def startApi(self):
  self.api = api()

 def startLogger(self):
  self.logger = logger(self.api)

 def startUser(self):
  self.user = user(self.api)
  self.api.user = self.user

 def setCurrencies(self, listType=0):
  # simple
  if listType == 1:
    self.currencies = [currency('ltc'), currency('btc'), currency('usd')]
  else:
    self.currencies = [currency('ltc'), currency('btc'), currency('usd'), currency('eur'), currency('rur')]

 def runForever(self, times):
  self.start()

  while times != 0:
    self.run()
    time.sleep(5)
    if times < 1000:
      times -= 1

 def runOnce(self):
  self.start()
  self.run()
 def run(self):
  startTime = datetime.now()


  #logger = logger(api)


  #api = api('EX5MTSTX-A816DXWK-UUDB68A5-BBGMQ2B5-1O144CWS','08caaaf52a9a83512a8b56323b628a293d173ce4565dceb645524b6c0542ecdb')

  print "3) get rates"
  self.api.getRates()

  print "4) create currencies"
  cutoff = 5
  print "5) get search"
  newSearch = search(self.api)
  print "6) solve search"
  searchTree = newSearch.findSolution(random.choice(self.currencies))

  print "total calculation time: %s" % ((datetime.now() - startTime).total_seconds())

  if searchTree[1][0] != "ltc":
    print "NOT LTC"
    time.sleep(0.5)
    return

  """if searchTree[2] <= 1.0:
    print "non-positive trade"
    time.sleep(0.5)
    return"""

  print "7) get user count"
  userCount = 1.0#self.user.getCurrency(searchTree[1][0])
  if not userCount:
    print "could not trade due to insufficient funds"
    sys.exit(0)
    
  print "using %s of %s" % (userCount, searchTree[1][0])


  #search.solveTree(searchTree[0])
  print "8) get trader"
  newTrader = trader(self.api, searchTree[1], searchTree[2])
  print "9) execute trader"
  traderResult = newTrader.executeChain(newTrader.chain, userCount)
  endTime = datetime.now()
  differenceTime = (endTime - startTime).total_seconds()
  print "10) write to logger"
  self.logger.write(traderResult, searchTree[1][0], searchTree[2], searchTree[1], differenceTime, datetime.now())

  print "final result: ", traderResult

  print "##3) get rates"
  self.api.getRates()

  print "##4) create currencies"
  cutoff = 5
  print "##5) get search"
  newSearch = search(self.api)
  print "##6) solve search"
  searchTree = newSearch.findSolution(random.choice(self.currencies))






if __name__ == '__main__':
  
  arbitrage = arbitrage()
  arbitrage.runForever(5000)





