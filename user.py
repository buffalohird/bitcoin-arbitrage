import time
from currency import currency
import random
import Queue
from copy import copy

class user:

 def __init__(self, api):
  self.api = api
  self.currencies = {}
  self.permissions = 0.0

  info = self.checkInfo()
  self.getPermissions(info)
  self.getFunds(info)



 def checkInfo(self): 
  info = self.api.getInfo()
  #print "checking info wadddddd", info
  if info['success'] == 0:
  	print "user getInfo() failure"
  	return info["return"]

  return info["return"]

 def getFunds(self, info):
  #info = self.checkInfo()
  currencies = info['funds']
  self.currencies['ltc'] = 1.0#float(currencies['ltc'])
  self.currencies['btc'] = 1.0#float(currencies['btc'])
  self.currencies['usd'] = 1.0#float(currencies['usd'])
  self.currencies['eur'] = 1.0#float(currencies['eur'])
  self.currencies['rur'] = 1.0#float(currencies['rur'])

 def getCurrency(self, currency):
 	return self.currencies[currency]


 def getPermissions(self, info):
  rights = info["rights"]
  if rights["info"] == 1 and rights["trade"] == 1:
  	self.permissions = 1.0
  	print "permissions done succesfully"
  	return
  else:
  	print "permissions not correct!"
  	return 
  print "rights: ", rights
