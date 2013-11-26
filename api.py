import httplib
import urllib
import json
import hashlib
import hmac
import time
import threading
import sys
from datetime import datetime

class api:
 __api_key        = 'M37SI38B-UVVQP8U7-BPDKIVMC-L91EZMRJ-SZUVB50X';
 __api_secret        = 'd1517932ad7d99d591d9c2b8a9940d8f55d64df516e579dfcf3df7f8ab3cec93';
 __nonce_v        = 1;

 def __init__(self):
  #self.__api_key = api_key
  #self.__api_secret = api_secret
  self.rates = {}
  self.user = None
  self.nonceAdjust = 0

 def __nonce(self):
   newNonce = int(str(time.time()).split('.')[0]) + self.nonceAdjust
   self.nonceAdjust += 1 
   self.__nonce_v = str(newNonce)

 def __signature(self, params):
  return hmac.new(self.__api_secret, params, digestmod=hashlib.sha512).hexdigest()

 def __api_call(self,method,params):
  self.__nonce()
  params['method'] = method
  params['nonce'] = str(self.__nonce_v)
  params = urllib.urlencode(params)
  headers = {"Content-type" : "application/x-www-form-urlencoded",
                      "Key" : self.__api_key,
                     "Sign" : self.__signature(params)}
  conn = httplib.HTTPSConnection("btc-e.com")
  conn.request("POST", "/tapi", params, headers)
  response = conn.getresponse()
  data = json.load(response)
  conn.close()
  return data
  
 def get_param(self, couple, param):
  conn = httplib.HTTPSConnection("btc-e.com")
  conn.request("GET", "/api/2/"+couple+"/"+param)
  response = conn.getresponse()
  data = json.load(response)
  conn.close()
  return data

 
 def getInfo(self):
  return self.__api_call('getInfo', {})

 def TransHistory(self, tfrom, tcount, tfrom_id, tend_id, torder, tsince, tend):
  params = {
   "from"        : tfrom,
   "count"        : tcount,
   "from_id"        : tfrom_id,
   "end_id"        : tend_id,
   "order"        : torder,
   "since"        : tsince,
   "end"        : tend}
  return self.__api_cal('TransHistory', params)
 
 def TradeHistory(self, tfrom, tcount, tfrom_id, tend_id, torder, tsince, tend, tpair):
  params = {
   "from"        : tfrom,
   "count"        : tcount,
   "from_id"        : tfrom_id,
   "end_id"        : tend_id,
   "order"        : torder,
   "since"        : tsince,
   "end"        : tend,
   "pair"        : tpair}
  return self.__api_call('TradeHistory', params)

 def ActiveOrders(self, tpair):
  params = { "pair" : tpair }
  return self.__api_call('ActiveOrders', params)

 def Trade(self, tpair, ttype, trate, tamount):
  params = {
   "pair"        : str(tpair),
   "type"        : str(ttype),
   "rate"        : str(trate),
   "amount"        : str(tamount)}
  return self.__api_call('Trade', params)

 def prepareTrade(self, type1, type2, quantity):
  backwards = self.getDirection(type1, type2)
  tpair = ""
  ttype = ""
  trate = ""
  tamount = ""

  if backwards:
    tpair = "%s_%s" % (type2, type1)
    ttype = "buy"
    trate = self.rates[tpair]
    """print "going backwards and expecting lower price for sell"
    print trate
    print 1.0 / self.rates["%s_%s" % (type1, type2)]
    time.sleep(1000)"""
    tamount = quantity * (1.0 / float(self.getRate(type1, type2)))
  else:
    tpair = "%s_%s" % (type1, type2)
    ttype = "sell"
    trate = self.rates[tpair]
    """print "going forwards and expecting higher price for buy"
    print trate
    print 1.0 / self.rates["%s_%s" % (type2, type1)]
    time.sleep(1000)"""
    tamount = quantity

  print '\n\n\n'
  print tpair, ttype, trate, tamount
  print self.getRate(type1, type2) * quantity
  print type1, type2
  print '\n\n\n'
  return [tpair, ttype, trate, tamount]

 def makeTrade(self, type1, type2, quantity):
  [tpair, ttype, trate,tamount] = self.prepareTrade(type1, type2, quantity)

  trate = trate + 4.0
  print tamount
  #returnData = self.Trade("ltc_usd","sell", "8.0", "1.0")
  returnData = self.Trade(tpair,ttype, trate, tamount)
  print returnData
  if returnData["success"] == 1:
    print "success!"
    newQuantity = returnData["return"]["received"]
    remains = returnData["return"]["remains"]
    if remains == quantity:
      print "Error: %s of %s remains, trade %s -> %s not executed" % (remains, quantity, type1, type2)
      return tamount * trate
      time.sleep(5)

    elif remains == 0.0:
      returnQuantity = returnData["return"]["funds"][type2] - user.getCurrency[type2]
      print returnQuantity
      return

  else:
    print "error making trade with types %s and %s quantity %s for tpair: %s, ttype: %s, trate: %s, tamount: %s" % (type1, type2, quantity, tpair, ttype, trate, tamount)
    sys.exit(1)

 def getDirection(self, type1, type2):
  if type1 == "ltc":
    if type2 == "btc":
      return 0
    if type2 == "usd":
      return 0
    else:
      print "invalid get direction pair %s and %s" % (type1, type2)
      return 2
  if type1 == "btc":
    if type2 == "usd":
      return 0
    else:
      return 1
  if type1 == "usd":
    return 1

  print "nothing returned yet by getDirection %s %s" % (type1, type2)


 def getRateThread(self, type1, type2):
  forwardString = "%s_%s" % (type1, type2)
  backwardString = "%s_%s" % (type2, type1)
  paramDictionary = self.get_param(forwardString, 'ticker')
  self.rates[forwardString] = float(paramDictionary["ticker"]["sell"])
  self.rates[backwardString] = 1.0 / float(paramDictionary["ticker"]["buy"])
  return

 def getRatesFull(self):
	ltc_usd = self.get_param('ltc_usd', 'ticker')
	self.rates["ltc_usd"] = float(ltc_usd["ticker"]["sell"])
	self.rates["usd_ltc"] = 1.0 / float(ltc_usd["ticker"]["buy"])

	ltc_eur = self.get_param('ltc_eur', 'ticker')
	self.rates["ltc_eur"] = float(ltc_eur["ticker"]["sell"])
	self.rates["eur_ltc"] = 1.0 / float(ltc_eur["ticker"]["buy"])

	ltc_rur = self.get_param('ltc_rur', 'ticker')
	self.rates["ltc_rur"] = float(ltc_rur["ticker"]["sell"])
	self.rates["rur_ltc"] = 1.0 / float(ltc_rur["ticker"]["buy"])

	ltc_btc = self.get_param('ltc_btc', 'ticker')
	self.rates["ltc_btc"] = float(ltc_btc["ticker"]["sell"])
	self.rates["btc_ltc"] = 1.0 / float(ltc_btc["ticker"]["buy"])

	btc_usd = self.get_param('btc_usd', 'ticker')
	self.rates["btc_usd"] = float(btc_usd["ticker"]["sell"])
	self.rates["usd_btc"] = 1.0 / float(btc_usd["ticker"]["buy"])

	btc_eur = self.get_param('btc_eur', 'ticker')
	self.rates["btc_eur"] = float(btc_eur["ticker"]["sell"])
	self.rates["eur_btc"] = 1.0 / float(btc_eur["ticker"]["buy"])

	btc_rur = self.get_param('btc_rur', 'ticker')
	self.rates["btc_rur"] = float(btc_rur["ticker"]["sell"])
	self.rates["rur_btc"] = 1.0 / float(btc_rur["ticker"]["buy"])

 def getRates(self):
  startTime = datetime.now()

  ltc_usd_thread = threading.Thread(target=self.getRateThread, args = ('ltc', 'usd'))
  ltc_usd_thread.daemon = True
  ltc_usd_thread.start()
  
  print "1 total calculation time: %s" % ((datetime.now() - startTime).total_seconds())

  ltc_btc_thread = threading.Thread(target=self.getRateThread, args = ('ltc', 'btc'))
  ltc_btc_thread.daemon = True
  ltc_btc_thread.start()
  
  print "2 total calculation time: %s" % ((datetime.now() - startTime).total_seconds())

  btc_usd_thread = threading.Thread(target=self.getRateThread, args = ('btc', 'usd'))
  btc_usd_thread.daemon = True
  btc_usd_thread.start()

  print "3 total calculation time: %s" % ((datetime.now() - startTime).total_seconds())

  btc_usd_thread.join()
  ltc_btc_thread.join()
  ltc_usd_thread.join()


  
 def getRate(self, type1, type2):
 	#ltc btc
 	returnType = type1 + "_" + type2
 	if returnType in self.rates.keys():
 		return self.rates[returnType]

 	return "error getting rate of %s _ %s" % (type1, type2)

 def getTrade(self, type1, type2):
 	#print str(type1), str(type2)
 	rate = self.getRate(type1, type2)
 	return 0.998 * rate 





