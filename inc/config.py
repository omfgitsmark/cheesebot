import discord
import sqlite3
from inc import misc

cfg = []

def loadConfig(bot):
	global cfg
	if not cfg:
		conn = sqlite3.connect('data/bot.db')
		c = conn.cursor()
		for srv in bot.servers:
			c.execute("SELECT * FROM config WHERE id=?", (srv.id,))
			rows = c.fetchall()
			if len(rows) > 0:
				cfg.append({"server" : srv.id, "topic": rows[0][1], "respond": rows[0][2], "info": rows[0][3], "help": rows[0][4], "invite": rows[0][5], "enableEmoji": rows[0][6], "defaultEmoji": rows[0][7], "nick": rows[0][8], "battlechannel": rows[0][9]})
			else:
				cfg.append({"server" : srv.id, "topic": "", "respond": 1, "info": "", "help": "", "invite": "", "enableEmoji": 1, "defaultEmoji": "", "nick": "", "battlechannel": ""})
				c.execute("INSERT INTO config VALUES (?,'',1,'','','',1,'','','')", (srv.id,))
		conn.commit()
		conn.close()
		misc.debug("Config Loaded.")
		
def saveConfig():
	global cfg
	conn = sqlite3.connect('data/bot.db')
	c = conn.cursor()
	for tmpcfg in cfg:
		c.execute("SELECT * FROM config WHERE id=?", (tmpcfg["server"],))
		rows = c.fetchall()
		if len(rows) > 0:
			c.execute("UPDATE config SET topic=?, respond=?, info=?, help=?, invite=?, enableEmoji=?, defaultEmoji=?, nick=?, battlechannel=? WHERE id=?", (tmpcfg["topic"], tmpcfg["respond"], tmpcfg["info"], tmpcfg["help"], tmpcfg["invite"], tmpcfg["enableEmoji"], tmpcfg["defaultEmoji"], tmpcfg["nick"], tmpcfg["battlechannel"], tmpcfg["server"],))
		else:
			c.execute("INSERT INTO config VALUES (?,?,?,?,?,?,?,?,?,?)", (int(tmpcfg["server"]), tmpcfg["topic"], tmpcfg["respond"], tmpcfg["info"], tmpcfg["help"], tmpcfg["invite"], tmpcfg["enableEmoji"], tmpcfg["defaultEmoji"], tmpcfg["nick"], tmpcfg["battlechannel"],))
	conn.commit()
	conn.close()
	misc.debug("Config Saved.")
	
def printConfig(bot):
	global cfg
	retstr = "```"
	for item in cfg:
		tmpsrv = bot.get_server(item["server"])
		retstr += tmpsrv.name + "\n    ID: " + item["server"] + "\n    Topic: \"" + item["topic"] + "\"\n    Respond: " + str(item["respond"]) + "\n\n" 
	retstr += "```"
	return retstr
	
	
def isUserBanned(user):
	conn = sqlite3.connect('data/bot.db')
	c = conn.cursor()
	c.execute("SELECT * FROM bans WHERE id=?",(user.id,))
	rows = c.fetchall()
	conn.close()
	if len(rows) > 0:
		return True
	return False
	
def getToken():
	conn = sqlite3.connect('data/bot.db')
	c = conn.cursor()
	c.execute("SELECT * FROM globalconfig WHERE name='token'")
	rows = c.fetchall()
	conn.close()
	if len(rows) > 0:
		return rows[0][1]
		
def getOwner():
	conn = sqlite3.connect('data/bot.db')
	c = conn.cursor()
	c.execute("SELECT * FROM globalconfig WHERE name='owner'")
	rows = c.fetchall()
	conn.close()
	if len(rows) > 0:
		return rows[0][1]
	