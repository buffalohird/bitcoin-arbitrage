class currency:

 def __init__(self, name):
  self.name = name
  self.successors = []
  if name == "ltc":
    self.successors = ['btc', 'usd']#, 'eur', 'rur']
  if name == "btc":
    self.successors = ['ltc', 'usd']#, 'eur', 'rur']
  if name == "usd":
    self.successors = ['ltc', 'btc']
  if name == "eur":
    self.successors = ['btc', 'ltc']
  if name == "rur":
    self.successors = ['btc', 'ltc']

 def __str__(self):
 	return "currency: %s" % (self.name)

