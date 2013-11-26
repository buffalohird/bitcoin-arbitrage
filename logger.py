import time
from currency import currency
import random
import Queue
from copy import copy
import csv
from datetime import datetime

class logger:

 def __init__(self, api):
  self.api = api
  self.data = []
  self.readFile('new.csv')


 def readFile(self, inputFile):
 	try:
 		with open(inputFile, 'rU') as csvFile:
		 	returnGrid = []
 			csvReader = csv.reader(csvFile)

 			if csvReader == []:
 				print "empty reader"
 				time.sleep(100)
 			for row in csvReader:
 				returnGrid.append(row)
 			self.data = returnGrid
 			return
 	except IOError:
 		print "IOERROR is raised. Error opening file %s with logger.py" % (str(inputFile)) 
 		self.writeStart()
 		#exit(1)

 def writeFile(self, outputFile):
 	with open(outputFile, 'w+') as writeFile:
 		csvWriter = csv.writer(writeFile)
 		for row in self.data:
 			csvWriter.writerow(row)

 def write(self, result, unit, gain, path, duration, date):
 	pathString = reduce(lambda x,y: x + ',' + y, path)
 	self.data.append([result, unit, gain, pathString, duration, date])

 def writeStart(self):
 	self.data.append(['final price', 'unit', 'raw ratio', 'path', 'duration(seconds)', 'date'])




