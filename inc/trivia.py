import discord
import json
import datetime
import sqlite3
import urllib
from inc import misc

class Trivia(object):
	active = False
	category = ""
	question = ""
	answer = ""
	hintchars = []
	channel = discord.Channel
	lastwinner = {}
	
	def __init__(self):
		self.question = 0;
		
	def load(self):
		conn = sqlite3.connect('data/bot.db')
		c = conn.cursor()
		if self.category:
			if self.category == "NOT_MUSIC":
				c.execute("SELECT * FROM trivia WHERE used=(SELECT min(used) FROM trivia WHERE LENGTH(answer)<30 AND NOT category='MUSIC') AND LENGTH(answer)<30 AND NOT category='MUSIC' ORDER BY RANDOM() LIMIT 1")
			else:
				c.execute("SELECT * FROM trivia WHERE used=(SELECT min(used) FROM trivia WHERE category=? AND LENGTH(answer)<30) AND LENGTH(answer)<30 AND category=? ORDER BY RANDOM() LIMIT 1", (self.category,self.category))
		else:
			c.execute("SELECT * FROM trivia WHERE used=(SELECT min(used) FROM trivia WHERE LENGTH(answer)<30) AND LENGTH(answer)<30 ORDER BY RANDOM() LIMIT 1")
		rows = c.fetchall()
		tmpid = rows[0][0]
		self.category = rows[0][1].replace("_"," ").title()
		self.question = self.cleanQ(rows[0][2])
		self.answer = rows[0][3]
		newused = rows[0][4] + 1
		try:
			c.execute("UPDATE trivia SET used=? WHERE id=?",(newused,tmpid))
		except:
			print("Failed to update used count.")
		conn.commit()
		conn.close()
		return True
		
	def start(self, msg):
		self.active = True
		self.hintchars = []
		self.channel = msg.channel
		retstr = ""
		if self.load():
			retstr += self.next()
		return retstr

	def stop(self):
		self.active = False
		
	def cleanQ(self, str):
		retstr = str
		retstr = retstr.replace("_","\_")
		retstr = retstr.replace("*","\*")
		retstr = retstr.replace("`","\`")
		retstr = retstr.replace("~","\~")
		return retstr
		
	def clean(self, str):
		retstr = str
		if "(" in str:
			arr = str.split("(")
			retstr = arr[0].strip()
		return retstr
		
	def next(self):
		return "**" + self.category + "**\n" + self.question + "?\n\n**HINT:**\n" + self.hint(False)
	
	def check(self, msg):
		retstr = ""
		txt = msg.content.lower()
		answer = self.clean(self.answer.lower())
		if answer in txt:
			return self.correct(msg)
		txtarr = txt.split(" ")
		ansarr = answer.split(" ")
		for txtword in txtarr:
			for answord in ansarr:
				changed = False
				if txtword == answord:
					start = answer.find(txtword)
					end = start + len(txtword)
					for i in range(start, end):
						if not self.hintchars[i]["show"]:
							self.hintchars[i]["show"] = True
							changed = True
					if changed:
						retstr = self.hint(False)		
		return retstr
	
	def correct(self, message):
		retstr = "**" + message.author.name + "** is correct!"
		try:
			if self.lastwinner["user"] == message.author:
				self.lastwinner["count"] += 1
				retstr += " *[" + str(self.lastwinner["count"]) + " streak]*"
			else:
				self.lastwinner = {"user":message.author,"count":1}
		except:
			self.lastwinner = {"user":message.author,"count":1}
		retstr += "\nThe answer was: **" + self.answer + "**"
		self.stop()
		conn = sqlite3.connect('data/bot.db')
		c = conn.cursor()
		c.execute("SELECT * FROM triviascores WHERE name=?", (message.author.name,))
		rows = c.fetchall()
		if len(rows) > 0:
			newscore = rows[0][2] + 1
			c.execute("UPDATE triviascores SET score=? WHERE name=?", (newscore, message.author.name))
		else:
			c.execute("INSERT INTO triviascores VALUES (NULL, ?, 1)", (message.author.name,))
		conn.commit()
		conn.close()
		return retstr
		
	def giveup(self):
		self.stop()
		self.lastwinner = {}
		return "The answer was: **" + self.answer + "**"
	
	def hint(self, next):
		retstr = "```\n"
		answer = self.clean(self.answer)
		if len(self.hintchars) == 0:
			next = False
			for i in range(0, len(answer)):
				char = answer[i:i+1]
				show = False
				if char == "," or char == "-" or char == "/" or char == "'" or char == "&" or char == "*" or char == "_" or char == "%" or char == "\"" or char == "$" or char == "#" or char == "@" or char == "!" or char == "~" or char == "+" or char == "=" or char == ":" or char == "." or char == "?" or char == " ":
					show = True
				self.hintchars.append({"char":char,"show":show})
		for i in range(0, len(self.hintchars)):
			if self.hintchars[i]["show"]:
				retstr += self.hintchars[i]["char"] + " "
			else:
				if next:
					next = False
					self.hintchars[i]["show"] = True
					retstr += self.hintchars[i]["char"] + " "
				else:
					retstr += "_ "
		retstr += "\n```"
		#print(retstr)
		return retstr
		
	def bighint(self):
		retstr = "```\n"
		start = False
		done = False
		for i in range(0, len(self.hintchars)):
			if start:
				if done:
					if self.hintchars[i]["show"]:
						retstr += self.hintchars[i]["char"] + " "
					else:
						retstr += "_ "
				else:
					if self.hintchars[i]["char"] == " ":
						done = True
					self.hintchars[i]["show"] = True
					retstr += self.hintchars[i]["char"] + " "
			else:
				if not self.hintchars[i]["show"]:
					start = True
				retstr += self.hintchars[i]["char"] + " "
		
		retstr += "```"
		return retstr
		
	def setCategory(self, txt):
		txt = txt.lower()
		self.category = ""
		if "arts and literature" in txt or "art" in txt or "literature" in txt:
			self.category = "ART_AND_LITERATURE"
		if "entertainment" in txt or "tv" in txt or "movie" in txt or "film" in txt:
			self.category = "ENTERTAINMENT"
		if "food and drink" in txt or "food" in txt or "drink" in txt:
			self.category = "FOOD_AND_DRINK"
		if "geography" in txt:
			self.category = "GEOGRAPHY"
		if "history" in txt:
			self.category = "HISTORY"
		if "language" in txt:
			self.category = "LANGUAGE"
		if "mathematics" in txt or "math" in txt:
			self.category = "MATHEMATICS"
		if "music" in txt:
			self.category = "MUSIC"
		if "people and places" in txt or "people" in txt or "places" in txt:
			self.category = "PEOPLE_AND_PLACES"
		if "religion and mythology" in txt or "religion" in txt or "mythology" in txt:
			self.category = "RELIGION_AND_MYTHOLOGY"
		if "science and nature" in txt or "science" in txt or "nature" in txt:
			self.category = "SCIENCE_AND_NATURE"
		if "sports and leisure" in txt or "sport" in txt or "leisure" in txt:
			self.category = "SPORT_AND_LEISURE"
		if "tech and video games" in txt or "tech" in txt or "video games" in txt:
			self.category = "TECH_AND_VIDEO_GAMES"
		if "toys and games" in txt or "toys" in txt:
			self.category = "TOYS_AND_GAMES"
		if "not music" in txt:
			self.category = "NOT_MUSIC"
		
	def categories(self):
		retstr = "```\n"
		retstr += "Art and Literature".ljust(25) + "\"art and literature\", \"art\", \"literature\"\n"
		retstr += "Entertainment".ljust(25) + "\"entertainment\"\n"
		retstr += "Food and Drink".ljust(25) + "\"food and drink\", \"food\", \"drink\"\n"
		retstr += "Geography".ljust(25) + "\"geography\"\n"
		retstr += "History".ljust(25) + "\"history\"\n"
		retstr += "Language".ljust(25) + "\"language\"\n"
		retstr += "Mathematics".ljust(25) + "\"mathematics\", \"math\"\n"
		retstr += "Music".ljust(25) + "\"music\"\n"
		retstr += "People and Places".ljust(25) + "\"people and places\", \"people\", \"places\"\n"
		retstr += "Religion and Mythology".ljust(25) + "\"religion and mythology\", \"religion\", \"mythology\"\n"
		retstr += "Science and Nature".ljust(25) + "\"science and nature\", \"science\", \"nature\"\n"
		retstr += "Sports and Leisure".ljust(25) + "\"sports and leisure\", \"sports\", \"leisure\"\n"
		retstr += "Tech and Video Games".ljust(25) + "\"tech and video games\", \"tech\", \"video games\"\n"
		retstr += "Toys and Games".ljust(25) + "\"toys and games\", \"toys\"\n"
		retstr += "```"
		return retstr
		
	def help(self, prefix):
		return "```\n" + prefix + "trivia".ljust(25) + "Starts a random trivia question.\n" + prefix + "trivia <category>".ljust(25) + "Asks a trivia question from specified category.\n" + prefix + "hint".ljust(25) + "Adds another letter to the hint.\n" + prefix + "bighint".ljust(25) + "Adds the next word to the hint.\n" + prefix + "giveup".ljust(25) + "Gives up on the current question. (Please try to not leave a question active)\n" + prefix + "triviacategories".ljust(25) + "List trivia categories.\n" + prefix + "triviascore".ljust(25) + "Shows your current score.\n" + prefix + "triviahelp".ljust(25) + "Shows this message.```\n**TIPS**```\n- Numbers will often be spelled out.\n- Special characters like \"-\" or \",\" will be shown in the hint automatically, but still need to be typed in your answer.\n- Correctly guessed words will show up in the hint, but points will not be given until the whole answer is guessed.\n- Spelling counts so type carefully!```"
		#retstr += "`" + prefix + "trivia`
		
	def score(self, message):
		testname = message.author.name
		if '"' in message.content:
			arr = message.content.split('"')
			testname = arr[1]
		if " " in message.content:
			arr = message.content.split(" ")
			if len(arr) > 1 and arr[1]:
				testname = arr[1]
		conn = sqlite3.connect('data/bot.db')
		c = conn.cursor()
		c.execute("SELECT * FROM triviascores WHERE name=?", (testname,))
		rows = c.fetchall()
		if len(rows) > 0:
			retstr = "**" + testname + "** currently has " + str(rows[0][2]) + " Points."
		else:
			retstr = "**" + testname + "** currently has 0 Points."
		conn.close()
		return retstr
		
	def handler(self, message, prefix):
		txt = message.content
		if txt.lower().startswith(prefix + "triviacategories"):
			return self.categories()
		if txt.lower().startswith(prefix + "triviascore"):
			return self.score(message)
		if txt.lower().startswith(prefix + "triviahelp"):
			return self.help(prefix)
		# .trivialeaderboard
		if txt.lower().startswith(prefix + "trivia"):
			if self.active:
				if message.channel == self.channel:
					return "There is already a question pending. Type `" + prefix + "giveup` to give up on the last question."
				else:
					return "I'm sorry, I am currently doing trivia in **#" + self.channel.name + "** on **" + self.channel.server.name + "**." 
			else:
				self.setCategory(txt)
				return self.start(message)
		if self.active and message.channel == self.channel:
			if txt.lower().startswith(prefix + "giveup"):
				return self.giveup()
			if txt.lower().startswith(prefix + "hint"):
				return self.hint(True)
			if txt.lower().startswith(prefix + "bighint"):
				return self.bighint()
			return self.check(message)
		
		
trivia = Trivia()