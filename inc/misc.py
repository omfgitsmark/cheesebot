#import discord
#import random
#import json
import sqlite3
import urllib.request
import datetime
import os
 
def setupDB():
	if not os.path.isfile('data/bot.db'):
		if not os.path.exists("data"):
			os.makedirs("data")
		conn = sqlite3.connect('data/bot.db')
		c = conn.cursor()
		c.execute("CREATE TABLE config ( `id` INTEGER NOT NULL, `topic` TEXT, `respond` INTEGER, `info` TEXT, `help` TEXT, `invite` TEXT, `enableEmoji` INTEGER, `defaultEmoji` TEXT, `nick` TEXT, `battlechannel` TEXT, PRIMARY KEY(`id`) )")
		c.execute("CREATE TABLE IF NOT EXISTS scores ( 'id' INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 'name' text, 'score' int )")
		c.execute("CREATE TABLE IF NOT EXISTS shitlist ( 'id' INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 'name' TEXT )")
		conn.commit()
		conn.close()
		print("Database Setup.")

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
	#if not os.path.exists("log"):
	#	os.makedirs("log")
	#appendFile("log/log.txt",str(datetime.datetime.now()) + " - " + txt + "\n")