#import discord
#import random
#import json
import urllib.request
import datetime

def getWebData(url):
	try:
		return urllib.request.urlopen(url).read()
	except:
		return "ERROR: Unable to connect"

def readFile(path):
	try:
		with open(path, "r") as file:
			return file.read()
	except:
		return "ERROR: Unable to open file."
		
def writeFile(path, data):
	try:
		with open(path, "w") as file:
			file.write(data)
	except:
		return "ERROR: Unable to write to file."
		
def appendFile(path, data):
	try:
		with open(path, "a") as file:
			file.write(data)
	except:
		try:
			with open(path, "w") as file:
				file.write(data)
		except:
			return "ERROR: Unable to write to file."
			
def debug(txt):
	print(txt)
	appendFile("log/log.txt",str(datetime.datetime.now()) + " - " + txt + "\n")