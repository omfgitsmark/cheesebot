import discord
import sqlite3

def convertToEmbed(row):
	multiverseid = row[2] # 2
	cardtype = row[41] # 41
	cardname = row[25] # 25
	manaCost = row[24] # 24
	rarity = row[32] # 32
	cardtext = row[39] # 39
	flavor = row[14] # 14
	power = row[30] # 30
	toughness = row[40] # 40
	if multiverseid == 0:
		txt = manaCost + "\n" + rarity + "\n" + cardtype
		if not cardtext == "":
			txt += "\n\n" + cardtext
		if not flavor == "":
			txt += "\n\n*" + flavor + "*"
		if cardtype.startswith("Creature"):
			txt += "\n\n`" + power + " / " + toughness + "`"
		ret = discord.Embed(title="", description=txt, color=0x363636, url="http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=" + str(multiverseid))
		ret.set_author(name=cardname, url="http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=" + str(multiverseid), icon_url="http://249d.com/dev/images/mtg_icon.png") 
		#embed.add_field(name="<:thonkang:219069250692841473>", value="these last two", inline=True)
	else:
		ret = discord.Embed(title="", description="", color=0x363636, url="http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=" + str(multiverseid))
		ret.set_image(url="http://gatherer.wizards.com/Handlers/Image.ashx?multiverseid=" + str(multiverseid) + "&type=card")
		ret.set_author(name=cardname, url="http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=" + str(multiverseid), icon_url="http://249d.com/dev/images/mtg_icon.png")
	return ret

def mtgHandler(msg, prefix):
	txt = msg.content
	if txt.lower().startswith(prefix + "mtg"):
		params = txt.lower().replace(prefix + "mtg", "")
		# extra handlers here
		return "Coming Soon!"
	if txt.find("[[") >= 0 and txt.find("]]") >= 0:
		start = txt.find("[[") + 2
		end = txt.find("]]")
		cardname = txt[start:end].lower()
		conn = sqlite3.connect('data/mtg.db')
		c = conn.cursor()
		c.execute("SELECT * FROM cards WHERE lower(name)=? ORDER BY multiverseId DESC LIMIT 1", (cardname,))
		rows = c.fetchall() # c.fetchone()
		if len(rows) > 0:
			conn.close()
			return convertToEmbed(rows[0])
		c.execute("SELECT * FROM cards WHERE lower(replace(name,\",\",\"\"))=? ORDER BY multiverseId DESC LIMIT 1", (cardname.replace(",",""),))
		rows = c.fetchall()
		if len(rows) > 0:
			conn.close()
			return convertToEmbed(rows[0])
		q = "SELECT * FROM cards WHERE name LIKE \"" + cardname[:0] + "%" + cardname[1:] + "\" "
		i = 1
		while i < len(cardname):
			q += "OR name LIKE \"" + cardname[:i] + "%" + cardname[i+1:] + "\" "
			i += 1
		q += "ORDER BY multiverseId DESC LIMIT 1"
		c.execute(q)
		rows = c.fetchall()
		if len(rows) > 0:
			conn.close()
			return convertToEmbed(rows[0])
		conn.close()
		return "**" + cardname + "** not found!"