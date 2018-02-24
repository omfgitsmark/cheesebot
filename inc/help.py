

def getHelp(msg, prefix):
	helpstr = ""
	arr = msg.content.split(" ")
	if len(arr) > 1:
		txt = arr[1]
		if txt.startswith(prefix): txt = txt.replace(prefix,"")
		if txt.lower() == "info":
			helpstr = "```\n" + prefix + "info\n\nPrints information about the bot.```"
		elif txt.lower() == "invite":
			helpstr = "```\n" + prefix + "invite\n\nPrints a link to invite someone to discord.```"
		elif txt.lower() == "topic":
			helpstr = "```\n" + prefix + "topic\n\nSets the current topic or prints the current topic if left blank.\n\nExamples:\n\n" + prefix + "topic\n" + prefix + "topic Whatever you want the topic to be\n" + prefix + "topic \"Whatever you want the topic to be\"```"
		elif txt.lower() == "roll":
			helpstr = "```\n" + prefix + "roll\n\nRolls the dice specified, or if none specified rolls 1-100. Uses the NdN format, where the first N is how many dice to roll, and the second N is how many sides the dice have.\nNOTE: Maximum number of rolls is 10 and maximum number of sides is 1,000,000\n\nExample:\n\n" + prefix + "roll 3d6```"
		elif txt.lower() == "choose":
			helpstr = "```\n" + prefix + "choose\n\nChoose between any number of options given.\n\nExamples:\n\n" + prefix + "choose option1 option2\n" + prefix + "choose \"option 1\" \"option 2\" \"option 3\"```"
		elif txt.lower() == "trivia":
			helpstr = "```\n" + prefix + "trivia\n\nAsks a random trivia question to the channel.\n\nExamples:\n\n" + prefix + "trivia```\n\n**NOTE:** Use `" + prefix + "triviahelp` for complete information."
		elif txt.lower() == "challenge":
			helpstr = "```\n" + prefix + "challenge\n\nChallenge a player to a battle, or issue an open challenge to everyone.\n\nExamples:\n\n" + prefix + "challenge\n" + prefix + "challenge @user#XXXX ```"
		elif txt.lower() == "deal":
			helpstr = "```\n" + prefix + "deal\n\nDeals you a 5 card hand. No real purpose yet, but fun.```"
		elif txt.lower() == "talk":
			helpstr = "```\n" + prefix + "talk\n\nMake the bot respond to certain statements.```"
		elif txt.lower() == "shutup":
			helpstr = "```\n" + prefix + "shutup\n\nStops the bot from responding.```"
		elif txt.lower() == "score":
			helpstr = "```\n" + prefix + "score\n\nPrints your current score if no name is given, otherwise the score of the person with the name given will be printed.\n\nExamples:\n\n" + prefix + "score\n" + prefix + "score SomeonesName```"
		elif txt.lower() == "leaderboard":
			helpstr = "```\n" + prefix + "leaderboard\n\nPrints the leaderboard.```"
		elif txt.lower() == "meme":
			helpstr = "```\n" + prefix + "meme\n\nDon't worry about it.```"
		elif txt.lower() == "cute":
			helpstr = "```\n" + prefix + "cute\n\nFor therapeutic purposes only. Prints a link to a cute picture. Enjoy responsibly.```"
		else: 
			helpstr = "Help topic not found. Good luck with that."
	else:
		helpstr = "```\n[GENERAL]\n\n"
		helpstr += "  " + prefix + "info".ljust(15) + "Prints bot information.\n"
		helpstr += "  " + prefix + "invite".ljust(15) + "Prints an invite link.\n"
		helpstr += "  " + prefix + "topic".ljust(15) + "Prints or Sets the current topic.\n"
		helpstr += "\n[TOOLS]\n\n"
		helpstr += "  " + prefix + "roll".ljust(15) + "Roll them dice. (Uses \"NdN\" format)\n"
		helpstr += "  " + prefix + "choose".ljust(15) + "Picks between multiple choices given.\n"
		helpstr += "\n[GAMES]\n\n"
		helpstr += "  " + prefix + "trivia".ljust(15) + "Asks a trivia queston.\n"
		helpstr += "  " + prefix + "challenge".ljust(15) + "Challenge someone to a battle.\n"
		helpstr += "  " + prefix + "deal".ljust(15) + "Deals you a poker hand.\n"
		helpstr += "\n[SETTINGS]\n\n"
		helpstr += "  " + prefix + "talk".ljust(15) + "Make the bot respond to certain statements.\n"
		helpstr += "  " + prefix + "shutup".ljust(15) + "Stops the bot from responding.\n"
		helpstr += "\n[EXTRAS]\n\n"
		helpstr += "  " + prefix + "score".ljust(15) + "Prints your current score.\n"
		helpstr += "  " + prefix + "leaderboard".ljust(15) + "Prints the leaderboard.\n"
		helpstr += "  " + prefix + "meme".ljust(15) + "Posts a random meme.\n"
		helpstr += "  " + prefix + "cute".ljust(15) + "For therapeutic purposes.\n"
		helpstr += "\nType \"" + prefix + "help <command>\" for more information on a command.```"
	return helpstr