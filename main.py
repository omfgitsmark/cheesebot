from discord.ext.commands import Bot
import random
from inc import battle, respond, cards, help, misc

bot_prefix = '.'
cheeseBot = Bot(command_prefix=bot_prefix)
#gt = trends.Trends()
deck = cards.Deck()
currenttopic = ""

@cheeseBot.event
async def on_ready():
	misc.debug("cheeseBot Online!")
    
@cheeseBot.event
async def on_message(message):
	if message.author.bot:
		return
	global bot_prefix
	# battle commands
	tmp = battle.handleMessage(message, bot_prefix)
	if tmp:
		return await cheeseBot.send_message(message.channel, tmp)
	# help command override
	if message.content.lower().startswith(bot_prefix + "help"):
		return await cheeseBot.send_message(message.channel, help.getHelp(message, bot_prefix))
	# Response handling
	tmpresponse = respond.getResponse(message)
	if tmpresponse:
		return await cheeseBot.send_message(message.channel, tmpresponse)
	return await cheeseBot.process_commands(message)

@cheeseBot.command(description='What do you not get about that?\n\nExample:')
async def info():
	"""Retrieves bot information."""
	return await cheeseBot.say('Hello, I am :cheese:**cheeseBot**!\nI was created by Mark, who is not very good at scripting so give him some time to make me worth something, and then I\'ll be open source.\n\nCheck out http://249d.com for more projects and information.')

@cheeseBot.command()
async def invite():
	"""Generates invite link."""
	return await cheeseBot.say("https://discord.gg/K5MqgPs")

@cheeseBot.command()
async def shutup():
	"""Shuts the bot up."""
	respond.autoRespond = 0
	return await cheeseBot.say("I'm sorry, I will be quiet now.")
	
@cheeseBot.command()
async def talk():
	"""Make the bot respond to certain statements."""
	respond.autoRespond = 1
	return await cheeseBot.say("Hello, how can I help?")

@cheeseBot.command(pass_context=True)
async def roll(ctx, NdN = "1d100"):
	"""Rolls them dice."""
	try:
		txt = ctx.message.content.replace(bot_prefix + "roll ","").replace(" ","")
		if "d" in txt.lower():
			vals = ctx.message.content.replace(bot_prefix + "roll ","").replace(" ","").split('d')
			try:
				rolls = int(vals[0])
			except:
				rolls = 1
			limit = int(vals[-1])
		else:
			rolls = 1
			limit = int(txt)
	except Exception:
		return await cheeseBot.say(":game_die: " + str(random.randint(1, 100)))
	note = ""
	if rolls > 10: 
		rolls = 10
		note += "*NOTE: Maximum number of rolls is 10.*\n"
	if limit > 1000000: 
		limit = 1000000
		note += "*NOTE: Maximum roll size is 1,000,000.*\n"
	result = note + ' '.join(" :game_die: " + str(random.randint(1, limit)) for r in range(rolls))
	await cheeseBot.say(result)

@cheeseBot.command(pass_context=True)
async def choose(ctx, Choice1="", Choice2="", etc=""):
	"""Picks between multiple choices given."""
	if '"' in ctx.message.content:
		vals = ctx.message.content.split('"')
	else:
		vals = ctx.message.content.split(' ')
	newvals = vals
	c = 0
	for val in vals:
		if val.replace(" ","") and val.lower().replace(" ","") != bot_prefix + "choose":
			newvals[c] = val
			c = c + 1
	if c < 2:
		return await cheeseBot.say("\"I need more choices!")
	final = vals[random.randint(0,c-1)]
	theword = "is"
	if final.lower().endswith("s"): theword = "are"
	await cheeseBot.say(":trophy: **" + final + "** " + theword + " the winner!")

@cheeseBot.command(pass_context=True)
async def meme(ctx):
	"""Posts a random meme."""
	misc.appendFile("data/shitlist.txt", ctx.message.author.name + "\n")
	return await cheeseBot.say("**" + ctx.message.author.name + "** is a dirty memer and has been added to the ShitList.")

@cheeseBot.command()
async def cute():
	"""For therapeutic purposes."""
	responses = {0: "http://249d.com/cute/1.jpg", 1: "http://249d.com/cute/2.jpg", 2: "http://249d.com/cute/3.png", 3: "http://249d.com/cute/4.jpg", 4: "http://249d.com/cute/5.png", 5: "http://249d.com/cute/6.jpg", 6: "http://249d.com/cute/7.jpg", 7: "http://249d.com/cute/8.jpg", 8: "http://249d.com/cute/9.png", 9: "http://249d.com/cute/10.jpg", 10: "http://249d.com/cute/11.jpg", 11: "http://249d.com/cute/12.jpg", 12: "http://249d.com/cute/13.JPG", 13: "http://249d.com/cute/14.png", 14: "http://249d.com/cute/15.png"}
	return await cheeseBot.say(responses[random.randint(0,14)])

@cheeseBot.command(pass_context=True)
async def score(ctx):
	"""Shows your current score."""
	testname = ctx.message.author.name
	if '"' in ctx.message.content:
		arr = ctx.message.content.split('"')
		testname = arr[1]
	if " " in ctx.message.content:
		arr = ctx.message.content.split(" ")
		if len(arr) > 1 and arr[1]:
			testname = arr[1]
	data = misc.readFile("data/scores.txt")
	for line in data.splitlines():
		if line.split(',')[0].lower() == testname.lower():
			return await cheeseBot.say("**" + testname + "** currently has " + line.split(',')[1] + " Points.")
	return await cheeseBot.say("**" + testname + "** currently has 0 Points.")

@cheeseBot.command(pass_context=True)
async def deal(ctx):
	"""Deal a poker hand."""
	global deck
	if " " in ctx.message.content:
		notestr = ""
		amount = 5
		try:
			amount = int(ctx.message.content.split(" ")[1])
			if amount > 26:
				amount = 26
				notestr = "*NOTE: Maximum number of dealt cards is 26*\n"
		except:
			amount = 5
		return await cheeseBot.say(notestr + deck.toString(deck.deal(amount)))
	else:
		return await cheeseBot.say(deck.toString(deck.deal(5)))
	
@cheeseBot.command()
async def shitlist():
	#try:
		d = misc.readFile("data/shitlist.txt")
		if d:
			d = "**Users currently on the ShitList:**\n" + d
			return await cheeseBot.say(d)
		else:
			return await cheeseBot.say("There is currently nobody on the Shit List!")
	#except:
	#	misc.debug("Error getting shitlist.txt")
	
	
@cheeseBot.command()
async def leaderboard():
	"""Shows the leaderboard."""
	all = []
	top5 = []
	data = misc.readFile("data/scores.txt")
	lines = data.splitlines()
	for line in lines:
		arr = line.split(',')
		try:
			all.append({"name":arr[0],"score":int(arr[1])})
		except:
			misc.debug("ERROR: Some user info in scores.txt may be corrupted.")
	for i in range(0,3):
		currentmax = 0
		currentuser = ""
		for entry in all:
			if not entry in top5:
				if entry["score"] > currentmax:
					currentuser = entry["name"]
					currentmax = entry["score"]
		top5.append({"name":currentuser, "score":currentmax})
	retstr = ""
	c = 0
	for entry in top5:
		if entry["name"]:
			if c == 0: retstr += ":first_place: "
			if c == 1: retstr += "    :second_place: "
			if c == 2: retstr += "        :third_place: "
			retstr += "**" + entry["name"] + "** [" + str(entry["score"]) + " points]\n"
			c += 1
	return await cheeseBot.say(retstr)
	
@cheeseBot.command()
async def scoreboard():
	"""Alias of leaderboard."""
	all = []
	top5 = []
	data = misc.readFile("data/scores.txt")
	lines = data.splitlines()
	for line in lines:
		arr = line.split(',')
		try:
			all.append({"name":arr[0],"score":int(arr[1])})
		except:
			misc.debug("ERROR: Some user info in scores.txt may be corrupted.")
	for i in range(0,3):
		currentmax = 0
		currentuser = ""
		for entry in all:
			if not entry in top5:
				if entry["score"] > currentmax:
					currentuser = entry["name"]
					currentmax = entry["score"]
		top5.append({"name":currentuser, "score":currentmax})
	retstr = ""
	c = 0
	for entry in top5:
		if entry["name"]:
			if c == 0: retstr += ":first_place: "
			if c == 1: retstr += "    :second_place: "
			if c == 2: retstr += "        :third_place: "
			retstr += "**" + entry["name"] + "** [" + str(entry["score"]) + " points]\n"
			c += 1
	return await cheeseBot.say(retstr)

@cheeseBot.command(pass_context=True)
async def topic(ctx):
	global currenttopic
	try:
		arr = ctx.message.content.split('"')
		if len(arr) > 1:
			currenttopic = arr[1]
			return await cheeseBot.say(":pencil2: **Topic Set:** " + currenttopic)
		if ctx.message.content.replace(bot_prefix + "topic ", "") and ctx.message.content.replace(bot_prefix + "topic", ""):
			currenttopic = ctx.message.content.replace(bot_prefix + "topic ", "")
			return await cheeseBot.say(":pencil2: **Topic Set:** " + currenttopic)
	except:
		misc.debug("Invalid topic format")
	if currenttopic:
		return await cheeseBot.say(":notepad_spiral: **Topic:** " + currenttopic)
	else:
		return await cheeseBot.say(":thought_balloon: No topic has been set. Say `" + bot_prefix + "topic \"Your topic here\"` to set the topic.")
	

cheeseBot.run("Token")
