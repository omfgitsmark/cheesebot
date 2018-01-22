import discord
import sqlite3
from inc import misc

cfg = []

def loadConfig(bot):
	if not cfg:
		for srv in bot.servers:
			cfg.append({"server" : srv.id, "topic": "", "respond": 1})
		misc.debug("Config setup complete.")
		
def saveConfig():
	#save to db
	txt = ""