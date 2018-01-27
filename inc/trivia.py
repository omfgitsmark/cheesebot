import json
import datetime
import sqlite3
import urllib
from inc import misc

class Trivia(object):
	scores = []
	data = None
	question = 0
	category = 0
	active = False
	hintchars = 0
	#lastqtime = datetime.datetime.now()
	
	def __init__(self):
		self.question = 0;
		
	def load(self):
		url = "https://opentdb.com/api.php?amount=5&difficulty=medium&type=multiple"
		if self.category > 0: url += "&category=" + str(self.category)
		data = misc.getWebData(url)
		tmpdata = json.loads(data)
		if tmpdata["response_code"] == 0:
			self.data = tmpdata["results"]
			return True
		return False
		
	def start(self):
		self.active = True
		retstr = ""
		self.question = 0
		self.hintchars = 0
		if self.load():
			retstr += self.next()
		return retstr

	def stop(self):
		self.active = False
		retstr = "Stopping Trivia!\n"
		retstr += self.end()
		return retstr
		
	def end(self):
		retstr = "Thanks for playing!\nQuestions provided by http://opentdb.com"
		return retstr
		
	def clean(self, str):
		str = str.replace('&quot;','"')
		str = str.replace('&#039;','\'')
		#str = urllib.unquote(str).decode('utf8')
		return str
		
	def next(self):
		validQ = False
		for i in range(self.question + 1, len(self.data)):
			self.data[i]["correct_answer"] = self.clean(self.data[i]["correct_answer"])
			if len(self.data[i]["correct_answer"]) < 20:
				if not "of these" in self.data[i]["question"].lower() and not "of the following" in self.data[i]["question"].lower():
					self.question = i
					validQ = True
					break
		if validQ:
			retstr = ""
			retstr += "**" + self.data[self.question]["category"] + "**\n" + self.clean(self.data[self.question]["question"]) + "\n\n**HINT:**\n"
			retstr += self.hint()
			return retstr
		else:
			print("No valid questions found, reloading.")
			self.load()
			self.question = 0
			return next()
	
	def correct(self, message):
		retstr = "**" + message.author.name + "** is correct!\nThe answer was: **" + self.data[self.question]["correct_answer"] + "**"
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
		retstr = "The answer was: **" + self.data[self.question]["correct_answer"] + "**"
		self.stop()
		return retstr
	
	def hint(self):
		answer = self.data[self.question]["correct_answer"]
		retstr = "```\n"
		if " " in answer:
			c = 0
			arr = answer.split(" ")
			ansclean = answer.replace(" ","").replace(",","").replace("-","")
			for word in arr:
				for i in range(0, len(word)):
					char = word[i:i+1]
					if char == "," or char == "-":
						retstr += char + " "
					else:
						if c < self.hintchars:
							retstr += ansclean[c:c+1] + " "
						else:
							retstr += "_ "
						c += 1
				retstr += "  "
		else:
			for i in range(0, len(answer)):
				char = answer[i:i+1]
				if char == "," or char == "-":
					retstr += char + " "
				else:
					if i < self.hintchars:
						retstr += answer[i:i+1] + " "
					else:
						retstr += "_ "
		retstr += "```"
		if self.hintchars < len(answer): 
			self.hintchars += 1
		return retstr
		
	def setCategory(self, name):
		self.category = 0
		if "general" in name.lower():
			self.category = 9
		if "books" in name.lower():
			self.category = 10
		if "film" in name.lower():
			self.category = 11
		if "music" in name.lower():
			self.category = 12
		if "theatre" in name.lower():
			self.category = 13
		if "tv" in name.lower():
			self.category = 14
		if "video games" in name.lower():
			self.category = 15
		if "board games" in name.lower():
			self.category = 16
		if "nature" in name.lower():
			self.category = 17
		if "computers" in name.lower():
			self.category = 18
		if "math" in name.lower():
			self.category = 19
		if "mythology" in name.lower():
			self.category = 20
		if "sports" in name.lower():
			self.category = 21
		if "geography" in name.lower():
			self.category = 22
		if "history" in name.lower():
			self.category = 23
		if "politics" in name.lower():
			self.category = 24
		if "art" in name.lower():
			self.category = 25
		if "celebrities" in name.lower():
			self.category = 26
		if "animals" in name.lower():
			self.category = 27
		if "vehicles" in name.lower():
			self.category = 28
		if "comics" in name.lower():
			self.category = 29
		if "gadgets" in name.lower():
			self.category = 30
		if "anime" in name.lower():
			self.category = 31
		if "cartoons" in name.lower():
			self.category = 32
		
	def categories(self):
		return "General\nBooks\nFilm\nMusic\nTheatre\nTV\nVideo Games\nBoard Games\nNature\nComputers\nMath\nMythology\nSports\nGeography\nHistory\nPolitics\nArt\nCelebrities\nAnimals\nVehicles\nComics\nGadgets\nAnime\nCartoons"
		
	def handler(self, message, prefix):
		txt = message.content
		if txt.lower().startswith(prefix + "triviacategories"):
			return self.categories()
		if txt.lower().startswith(prefix + "triviascore"):
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
		if txt.lower().startswith(prefix + "trivia"):
			if self.active:
				return "There is already a question pending. Type `" + prefix + "giveup` to give up on the last question."
			else:
				self.setCategory(txt)
				return self.start()
		if self.active:
			if self.data[self.question]["correct_answer"].lower() in txt.lower():
				return self.correct(message)
			#if txt.lower().startswith(prefix + "stoptrivia"):
			#	return self.stop()
			#if txt.lower().startswith(prefix + "next"):
			#	return self.next()
			if txt.lower().startswith(prefix + "giveup"):
				return self.giveup()
			if txt.lower().startswith(prefix + "hint"):
				return self.hint()
		
		
		
trivia = Trivia()