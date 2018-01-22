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
				cfg.append({"server" : srv.id, "topic": rows[0][1], "respond": rows[0][2]})
			else:
				cfg.append({"server" : srv.id, "topic": "", "respond": 1})
				c.execute("INSERT INTO config VALUES (?,'',1)", (srv.id,))
		conn.commit()
		conn.close()
		misc.debug("Config Setup Complete.")
		
def saveConfig():
	global cfg
	conn = sqlite3.connect('data/bot.db')
	c = conn.cursor()
	for tmpcfg in cfg:
		c.execute("SELECT * FROM config WHERE id=?", (tmpcfg["server"],))
		rows = c.fetchall()
		if len(rows) > 0:
			c.execute("UPDATE config SET topic=?, respond=? WHERE id=?", (tmpcfg["topic"], tmpcfg["respond"], tmpcfg["server"],))
		else:
			c.execute("INSERT INTO config VALUES (?,?,?)", (int(tmpcfg["server"]), tmpcfg["topic"], tmpcfg["respond"],))
	conn.commit()
	conn.close()
	misc.debug("Config Saved.")