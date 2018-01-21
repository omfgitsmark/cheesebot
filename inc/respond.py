import discord
import random
from inc import misc

autoRespond = 1

def getResponse(msg):
	try:
		txt = msg.content.lower()
		global autoRespond
		if autoRespond > 0:
			if "cheesebot" in txt:
				words = ["how are you?", "how are you doing?", "how are you,", "how are you doing,", "how are you doin?", "how are you doin,"
				if any(word in txt for word in words):
					responses = {0: "I am doing well. How are you, " + msg.author.name + "?", 1: "I am great, how are you today?"}
					return responses[random.randint(0,1)]
				else:
					responses = {0: "Are you talking about me, " + msg.author.name + "?", 1: "I'm just a robot, leave me alone."}
					return responses[random.randint(0,1)]
		words = ['nigger', 'guido', 'chink', 'jew', 'jews', 'spick', 'spic', ' coon', 'camel jockey', 'sand monkey', 'wetback', 'beaner', 'gook', 'kyke', 'nigga', 'burr head']
		if any(word in txt for word in words):
			try:
				data = misc.readFile("data/scores.txt")
				exists = False
				current = 0
				for line in data.splitlines():
					if line:
						arr = line.split(',')
						if str(arr[0]) == str(msg.author.name):
							current = int(arr[1])
							exists = True
				if exists:
					newcurrent = current + 1
					data = data.replace(msg.author.name + "," + str(current), msg.author.name + "," + str(newcurrent))
					misc.writeFile("data/scores.txt", data);
				else:
					misc.appendFile("data/scores.txt", msg.author.name + ",1\n")
			except:
				print("Error saving score.")
			return "**" + msg.author.name + "** was awarded +1 points for racism."
		words = ['faggot', 'fag', 'queer']
		if any(word in txt for word in words):
			try:
				data = misc.readFile("data/scores.txt")
				exists = False
				current = 0
				for line in data.splitlines():
					if line:
						arr = line.split(',')
						if str(arr[0]) == str(msg.author.name):
							current = int(arr[1])
							exists = True
				if exists:
					newcurrent = current + 1
					data = data.replace(msg.author.name + "," + str(current), msg.author.name + "," + str(newcurrent))
					misc.writeFile("data/scores.txt", data);
				else:
					misc.appendFile("data/scores.txt", msg.author.name + ",1\n")
			except:
				print("Error saving score.")
			return "**" + msg.author.name + "** was awarded +1 points for intolerance."	
		words = ['sideways vagina', 'sideways cunt', 'sideways pussy']
		responses = {0: "I'd still hit it.", 1: "I'll just turn my body when I put it in, no big deal."}
		if any(word in txt for word in words):
			return responses[random.randint(0,1)]
	except:
		print("Generic Error in getResponse")
		
