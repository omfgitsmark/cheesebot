import discord
import random
import sqlite3
from inc import misc

def getResponse(msg):
	#try:
		txt = msg.content.lower()
		if "cheesebot" in txt:
			words = ["how are you?", "how are you doing?", "how are you,", "how are you doing,", "how are you doin?", "how are you doin,"]
			if any(word in txt for word in words):
				responses = {0: "I am doing well. How are you, " + msg.author.name + "?", 1: "I am great, how are you today?"}
				return responses[random.randint(0,1)]
			else:
				responses = {0: "Are you talking about me, " + msg.author.name + "?", 1: "I'm just a robot, leave me alone."}
				return responses[random.randint(0,1)]
		words = ['nigger', 'guido', 'chink', 'jew', 'jews', 'spick', 'spic', ' coon', 'camel jockey', 'sand monkey', 'wetback', 'beaner', 'gook', 'kyke', 'nigga', 'burr head']
		if any(word in txt for word in words):
			conn = sqlite3.connect('data/bot.db')
			c = conn.cursor()
			c.execute("SELECT * FROM scores WHERE name=?", (msg.author.name,))
			rows = c.fetchall()
			if len(rows) > 0:
				newscore = rows[0][2] + 1
				c.execute("UPDATE scores SET score=? WHERE name=?", (newscore, msg.author.name))
			else:
				c.execute("INSERT INTO scores VALUES (NULL, ?, 1)", (msg.author.name,))
			conn.commit()
			conn.close()
			return "**" + msg.author.name + "** was awarded +1 points for racism."
		words = ['faggot', 'fag', 'queer']
		if any(word in txt for word in words):
			conn = sqlite3.connect('data/bot.db')
			c = conn.cursor()
			c.execute("SELECT * FROM scores WHERE name=?", (msg.author.name,))
			rows = c.fetchall()
			if len(rows) > 0:
				newscore = rows[0][2] + 1
				c.execute("UPDATE scores SET score=? WHERE name=?", (newscore, msg.author.name))
			else:
				c.execute("INSERT INTO scores VALUES (NULL, ?, 1)", (msg.author.name,))
			conn.commit()
			conn.close()
			return "**" + msg.author.name + "** was awarded +1 points for intolerance."	
		words = ['sideways vagina', 'sideways cunt', 'sideways pussy']
		responses = {0: "I'd still hit it.", 1: "I'll just turn my body when I put it in, no big deal."}
		if any(word in txt for word in words):
			return responses[random.randint(0,1)]
	#except:
	#	print("Generic Error in getResponse")
		
