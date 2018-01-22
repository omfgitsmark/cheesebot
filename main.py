import discord
from discord.ext.commands import Bot
import random
import sqlite3
from inc import battle, respond, cards, help, config, misc

bot_prefix = '.'
cheeseBot = Bot(command_prefix=bot_prefix)
deck = cards.Deck()

@cheeseBot.event
async def on_ready():
	# do DB setup on initial run
	misc.debug("cheeseBot Online!")
	config.loadConfig(cheeseBot)
    
@cheeseBot.event
async def on_message(message):
	if message.author.bot:
		return
	global bot_prefix
	# config print command
	if message.content.lower().startswith(bot_prefix + "config"):
		retstr = "```"
		for cfg in config.cfg:
			tmpsrv = cheeseBot.get_server(cfg["server"])
			retstr += "Name = " + tmpsrv.name + " | ID = " + cfg["server"] + " | Topic = \"" + cfg["topic"] + "\" | Respond = " + str(cfg["respond"]) + "\n" 
		retstr += "```"
		return await cheeseBot.send_message(message.channel, retstr)
	# battle commands
	tmp = battle.handleMessage(message, bot_prefix)
	if tmp:
		return await cheeseBot.send_message(message.channel, tmp)
	# help command override
	if message.content.lower().startswith(bot_prefix + "help"):
		return await cheeseBot.send_message(message.channel, help.getHelp(message, bot_prefix))
	# Response handling
	for i in config.cfg:
		if i["server"] == message.server.id:
			if i["respond"] > 0:
				tmpresponse = respond.getResponse(message)
				if tmpresponse:
					return await cheeseBot.send_message(message.channel, tmpresponse)
	# Default command handling
	return await cheeseBot.process_commands(message)

@cheeseBot.command()
async def info():
	"""Retrieves bot information."""
	return await cheeseBot.say('Hello, I am :cheese:**cheeseBot**!\n Find me at: https://github.com/omfgitsmark/cheesebot \n\nCheck out http://249d.com for more projects and information.')

@cheeseBot.command()
async def invite():
	"""Generates invite link."""
	return await cheeseBot.say("https://discord.gg/K5MqgPs")

@cheeseBot.command(pass_context=True)
async def shutup(ctx):
	"""Shuts the bot up."""
	for i in config.cfg:
		if i["server"] == ctx.message.server.id:
			i["respond"] = 0
			config.saveConfig()
			return await cheeseBot.say("I'm sorry, I will be quiet now.")
	
@cheeseBot.command(pass_context=True)
async def talk(ctx):
	"""Make the bot respond to certain statements."""
	for i in config.cfg:
		if i["server"] == ctx.message.server.id:
			i["respond"] = 1
			config.saveConfig()
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
	conn = sqlite3.connect('data/bot.db')
	c = conn.cursor()
	c.execute("INSERT INTO shitlist VALUES (NULL,?)", (ctx.message.author.name,))
	conn.commit()
	conn.close()
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
	# DB
	conn = sqlite3.connect('data/bot.db')
	c = conn.cursor()
	c.execute("SELECT * FROM scores WHERE name=?", (testname,))
	rows = c.fetchall()
	if len(rows) > 0:
		await cheeseBot.say("**" + testname + "** currently has " + str(rows[0][2]) + " Points.")
	else:
		await cheeseBot.say("**" + testname + "** currently has 0 Points.")
	conn.close()

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
	retstr = ""
	conn = sqlite3.connect('data/bot.db')
	c = conn.cursor()
	c.execute("SELECT * FROM shitlist")
	rows = c.fetchall()
	for row in rows:
		retstr += row[1] + "\n"
	conn.close()
	if retstr:
		retstr = "**Users currently on the ShitList:**\n" + retstr
		return await cheeseBot.say(retstr)
	else:
		return await cheeseBot.say("There is currently nobody on the Shit List!")	
	
@cheeseBot.command()
async def leaderboard():
	"""Shows the leaderboard."""
	retstr = ""
	conn = sqlite3.connect('data/bot.db')
	c = conn.cursor()
	c.execute("SELECT * FROM scores ORDER BY score DESC")
	rows = c.fetchall()
	if len(rows) >= 3:
		length = 3
	else:
		length = len(rows)
	for i in range(0, length):
		if i == 0: retstr += ":first_place: "
		if i == 1: retstr += "    :second_place: "
		if i == 2: retstr += "        :third_place: "
		retstr += "**" + rows[i][1] + "** [" + str(rows[i][2]) + " points]\n"
	conn.close()
	return await cheeseBot.say(retstr)
	
@cheeseBot.command()
async def scoreboard():
	"""Alias of leaderboard."""
	retstr = ""
	conn = sqlite3.connect('data/bot.db')
	c = conn.cursor()
	c.execute("SELECT * FROM scores ORDER BY score DESC")
	rows = c.fetchall()
	if len(rows) >= 3:
		length = 3
	else:
		length = len(rows)
	for i in range(0, length):
		if i == 0: retstr += ":first_place: "
		if i == 1: retstr += "    :second_place: "
		if i == 2: retstr += "        :third_place: "
		retstr += "**" + rows[i][1] + "** [" + str(rows[i][2]) + " points]\n"
	conn.close()
	return await cheeseBot.say(retstr)

@cheeseBot.command(pass_context=True)
async def topic(ctx):
	arr = ctx.message.content.split('"')
	if len(arr) > 1:
		for i in config.cfg:
			if i["server"] == ctx.message.server.id:
				i["topic"] = arr[1]
				config.saveConfig()
				return await cheeseBot.say(":pencil2: **Topic Set:** " + i["topic"])
	if ctx.message.content.replace(bot_prefix + "topic ", "") and ctx.message.content.replace(bot_prefix + "topic", ""):
		for i in config.cfg:
			if i["server"] == ctx.message.server.id:
				i["topic"] = ctx.message.content.replace(bot_prefix + "topic ", "")
				config.saveConfig()
				return await cheeseBot.say(":pencil2: **Topic Set:** " + i["topic"])
		
	for i in config.cfg:
		if i["server"] == ctx.message.server.id:
			if i["topic"]:
				return await cheeseBot.say(":notepad_spiral: **Topic:** " + i["topic"])
			else:
				return await cheeseBot.say(":thought_balloon: No topic has been set. Say `" + bot_prefix + "topic \"Your topic here\"` to set the topic.")
	
	
cheeseBot.run("secret")
