import discord
from discord.ext.commands import Bot
import random
import sqlite3
from inc import battle, respond, cards, help, config, trivia, misc

bot_prefix = '.'
cheeseBot = Bot(command_prefix=bot_prefix)

@cheeseBot.event
async def on_ready():
	misc.debug("cheeseBot Online!")
	config.loadConfig(cheeseBot)
    
@cheeseBot.event
async def on_message(message):
	if message.author.bot: return
	if config.isUserBanned(message.author): return
	global bot_prefix
	# trivia handling
	tmp = trivia.trivia.handler(message, bot_prefix)
	if tmp: return await cheeseBot.send_message(message.channel, tmp)
	# config print command
	if message.content.lower().startswith(bot_prefix + "config"):
		if message.author.id == config.getOwner():
			return await cheeseBot.send_message(message.channel, config.printConfig(cheeseBot))
	# battle commands
	tmp = battle.handleMessage(message, bot_prefix)
	if tmp: return await cheeseBot.send_message(message.channel, tmp)
	# help command override
	if message.content.lower().startswith(bot_prefix + "help"):
		return await cheeseBot.send_message(message.channel, help.getHelp(message, bot_prefix))
	# Response handling
	if not message.server:
		tmpresponse = respond.getResponse(message)
		if tmpresponse:
			return await cheeseBot.send_message(message.author, tmpresponse)
	else:
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

@cheeseBot.command(pass_context=True)
async def invite(ctx):
	"""Generates invite link."""
	if ctx.message.server.id == "331919313801969667":
		return await cheeseBot.say("https://discord.gg/K5MqgPs")
	if ctx.message.server.id == "222412917365145601":
		return await cheeseBot.say("https://discord.gg/5tnDXvZ")

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
	conn = sqlite3.connect('data/bot.db')
	c = conn.cursor()
	c.execute("SELECT * FROM cute ORDER BY RANDOM() LIMIT 1")
	rows = c.fetchall()
	retstr = rows[0][1]
	conn.commit()
	conn.close()
	return await cheeseBot.say(retstr)
	
@cheeseBot.command(pass_context=True)
async def addcute(ctx):
	"""Adds a link to the cute list."""
	arr = ctx.message.content.split(" ")
	addval = arr[1]
	if addval.lower().startswith("http://") or addval.lower().startswith("https://"):
		if addval.lower().endswith(".jpg") or addval.lower().endswith(".png") or addval.lower().endswith(".gif"):
			conn = sqlite3.connect('data/bot.db')
			c = conn.cursor()
			c.execute("INSERT INTO cute VALUES(NULL, ?)",(addval,))
			conn.commit()
			conn.close()
			return await cheeseBot.say("Successfully added!")
		else:
			return await cheeseBot.say("Must be a valid image!")
	else:
		return await cheeseBot.say("Must be a valid link!")
	
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
		return await cheeseBot.say(notestr + cards.deck.toString(cards.deck.deal(amount)))
	else:
		return await cheeseBot.say(cards.deck.toString(cards.deck.deal(5)))
	
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
				
@cheeseBot.command(pass_context=True)
async def award(ctx):	
	if len(ctx.message.mentions) > 0:
		name = ctx.message.mentions[0].name
	else:
		name = ctx.message.content.replace(bot_prefix + "award", "").strip()
	if name:
		conn = sqlite3.connect('data/bot.db')
		c = conn.cursor()
		c.execute("SELECT * FROM scores WHERE name=?", (name,))
		rows = c.fetchall()
		if len(rows) > 0:
			newscore = rows[0][2] + 1
			c.execute("UPDATE scores SET score=? WHERE name=?", (newscore, name))
		else:
			c.execute("INSERT INTO scores VALUES (NULL, ?, 1)", (name,))
		conn.commit()
		conn.close()
		return await cheeseBot.say("**" + name + "** has been awarded 1 point!")	
	else:
		return await cheeseBot.say("Please provide a user to award points to!")
		
#@cheeseBot.command(pass_context=True)
#async def test(ctx):			
#	return await cheeseBot.send_message(ctx.message.author, "test")
		
cheeseBot.run(config.getToken())
