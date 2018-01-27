import discord
import random
import datetime
#import asyncio # use to create background task checking for idle battles to cancel

battles = []

class Player(object):
	user = discord.User()
	hp = 100
	maxhp = 100
	mp = 50
	maxmp = 50
	initiative = 0
	attack = 0
	defense = 0
	dexterity = 0
	intelligence = 0
	battleclass = ""
	status = "" # poison, bleed, etc.
	
	def __init__(self, newuser):
		self.user = newuser;

class Battle(object):
	challenger = Player(discord.User)
	challengee = Player(discord.User)
	server = discord.Server
	channel = discord.Channel
	challengerGoesFirst = True
	state = "Awaiting Opponent"
	turn = 0
	turnstate = 0
	starttime = datetime.datetime.now()
	updatetime = datetime.datetime.now()
		
	def __init__(self, cer, cee, srv, chan):
		self.challenger = Player(cer)
		self.challengee = Player(cee)
		self.server = srv
		self.channel = chan
		self.challengerGoesFirst = random.randint(0,1) > 0
		
	def setClass(self, user, classname):
		retstr = ""
		if user == self.challenger.user:
			self.challenger.battleclass = classname
			if classname == "warrior":
				retstr += ":crossed_swords: "
				self.challenger.maxhp = 120
				self.challenger.hp = 120
				self.challenger.maxmp = 20
				self.challenger.mp = 20
				self.challenger.attack = 18
				self.challenger.defense = 16
				self.challenger.dexterity = 10
				self.challenger.intelligence = 6
			if classname == "wizard":
				retstr += ":scroll: "
				self.challenger.maxhp = 80
				self.challenger.hp = 80
				self.challenger.maxmp = 50
				self.challenger.mp = 50
				self.challenger.attack = 10
				self.challenger.defense = 6
				self.challenger.dexterity = 16
				self.challenger.intelligence = 18
			if classname == "ranger":
				retstr += ":bow_and_arrow: "
				self.challenger.maxhp = 100
				self.challenger.hp = 100
				self.challenger.maxmp = 30
				self.challenger.mp = 30
				self.challenger.attack = 15
				self.challenger.defense = 10
				self.challenger.dexterity = 15
				self.challenger.intelligence = 10
		else:
			self.challengee.battleclass = classname
			if classname == "warrior":
				retstr += ":crossed_swords: "
				self.challengee.maxhp = 120
				self.challengee.hp = 120
				self.challengee.maxmp = 20
				self.challengee.mp = 20
				self.challengee.attack = 18
				self.challengee.defense = 16
				self.challengee.dexterity = 10
				self.challengee.intelligence = 6
			if classname == "wizard":
				retstr += ":scroll: "
				self.challengee.maxhp = 80
				self.challengee.hp = 80
				self.challengee.maxmp = 50
				self.challengee.mp = 50
				self.challengee.attack = 10
				self.challengee.defense = 6
				self.challengee.dexterity = 16
				self.challengee.intelligence = 18
			if classname == "ranger":
				retstr += ":bow_and_arrow: "
				self.challengee.maxhp = 100
				self.challengee.hp = 100
				self.challengee.maxmp = 30
				self.challengee.mp = 30
				self.challengee.attack = 15
				self.challengee.defense = 10
				self.challengee.dexterity = 15
				self.challengee.intelligence = 10
		return "**" + user.name + "** has chosen " + classname + "!"
		
	def isPlayersTurn(self, user):
		if user == self.challenger.user:
			if self.challengerGoesFirst and self.turnstate == 0: return True
			if not self.challengerGoesFirst and self.turnstate == 1: return True
		elif user == self.challengee.user:
			if self.challengerGoesFirst and self.turnstate == 1: return True
			if not self.challengerGoesFirst and self.turnstate == 0: return True
		return False
		
	def isInBattle(self, user):
		if user == self.challenger.user or user == self.challengee.user:
			return True
	
	def isOpponentDead(self, user):
		if user == self.challenger.user:
			if self.challengee.hp <= 0: return True
		else:
			if self.challenger.hp <= 0: return True
			
	def attack(self, user): # NOTE: user is the attacking player
		retstr = ""
		if random.randint(0,100) == 0:
			retstr += ":hole: **" + user.name + "'s** attack missed!\n"
		else:
			dmg = 15 + random.randint(0, 25)
			retstr += ":boom: "
			if user == self.challenger.user:
				self.challengee.hp -= dmg
				if self.challengee.hp <= 0:
					self.challengee.hp = 0
				retstr += "**" + user.name + "** hit **" + self.challengee.user.name + "** for " + str(dmg) + " damage!\n"
			else:
				self.challenger.hp -= dmg
				if self.challenger.hp <= 0:
					self.challenger.hp = 0
				retstr += "**" + user.name + "** hit **" + self.challenger.user.name + "** for " + str(dmg) + " damage.\n"
		
		self.next()
		return retstr
	
	def heal(self, user):
		hhp = random.randint(20,40)
		if user == self.challenger.user:
			hhp += random.randint(0,self.challenger.intelligence)
			self.challenger.hp += hhp
		else:
			hhp += random.randint(0,self.challengee.intelligence)
			self.challengee.hp += hhp
		self.next()
		return ":revolving_hearts: **" + user.name + "** healed for " + str(hhp) + " HP!\n"
		
	def status(self):
		if self.state == "Awaiting Opponent":
			if self.challengee.user:
				return ":hourglass_flowing_sand: **" + self.challenger.user.name + "**  vs.  **" + self.challengee.user.name + "** | " + self.state + " | Turn 1"
			else:
				return ":bar_chart: **" + self.challenger.user.name + "**  vs.  **<OPEN>** | " + self.state + " | Turn 1"
		elif self.state == "Choosing Loadouts":
			return ":clipboard: **" + self.challenger.user.name + "**  vs.  **" + self.challengee.user.name + "** | " + self.state + " | Turn 1"
		elif self.state == "In Combat":
			return ":crossed_swords: **" + self.challenger.user.name + "** (" + self.challenger.battleclass +") **HP:** " + str(self.challenger.hp) + "/" + str(self.challenger.maxhp) + "  **MP:** " + str(self.challenger.mp) + "/" + str(self.challenger.maxmp) + "  vs.  **" + self.challengee.user.name + "** (" + self.challengee.battleclass +") **HP:** " + str(self.challengee.hp) + "/" + str(self.challengee.maxhp) + "  **MP:** " + str(self.challengee.mp) + "/" + str(self.challengee.maxmp)
	
	def options(self, prefix):
		retstr = ""
		if self.state == "Awaiting Opponent":
			retstr = ""
		if self.state == "Choosing Loadouts":
			return "**Both players please choose your class:**\n:crossed_swords: `" + prefix + "warrior".ljust(12) + "(Heavy attacker with good defense)`\n:scroll: `" + prefix + "wizard".ljust(12) + "(Best special abilities but soft as butter)`\n:bow_and_arrow: `" + prefix + "ranger".ljust(12) + "(All around with good attack, defense, and special abilities)`"
		if self.state == "In Combat":
			if self.turnstate > 0:
				if self.challengerGoesFirst:
					retstr += "**" + self.challengee.user.name + "'s turn, choose an option:**"
				else: 
					retstr += "**" + self.challenger.user.name + "'s turn, choose an option:**"
			else:
				if self.challengerGoesFirst:
					retstr += "**" + self.challenger.user.name + "'s turn, choose an option:**"
				else: 
					retstr += "**" + self.challengee.user.name + "'s turn, choose an option:**"
			# :skull: :footprints: 
			retstr += "\n:punch: `" + prefix + "attack".ljust(12) + "(Basic attack)`\n:comet: `" + prefix + "abilities".ljust(12) + "(List abilities)`\n:runner: `" + prefix + "run".ljust(12) + "(Run away and forfeit)`\n"
		return retstr
	
	def abilities(self, user, prefix):
		retstr = ""
		classstr = ""
		if user == self.challenger:
			classstr = self.challenger.battleclass
		else:
			classstr = self.challengee.battleclass
		if classstr == "warrior":
			retstr += ":heart:  `" + prefix + "heal".ljust(12) + "[-10MP]".ljust(10) + "(Heals a small amount of HP.)`"
		elif classstr == "wizard":
			retstr += ":revolving_hearts:  `" + prefix + "heal".ljust(12) + "[-10MP]".ljust(10) + "(Heals a small amount of HP.)`"
		elif classstr == "ranger":
			retstr += ":revolving_hearts:  `" + prefix + "heal".ljust(12) + "[-10MP]".ljust(10) + "(Heals a small amount of HP.)`"
		return retstr
		
	def run(self, user):
		if user == self.challenger.user:
			opp = self.challengee.user.name
		else:
			opp = self.challenger.user.name
		return ":hatching_chick: **" + user.name + "** has run away!\n\n:trophy: **" + opp + "** is the winner!"	
	
	def forfeit(self, user):
		if user == self.challenger.user:
			if self.challengee.user: 
				opp = self.challengee.user.name
			else:
				":x: **" + user.name + "** has canceled his challenge!"
		else:
			if self.challengee.user:
				opp = self.challenger.user.name
			else:
				":x: **" + user.name + "** has canceled his challenge!"
		return ":flag_white: **" + user.name + "** has forfeit!\n\n:trophy: **" + opp + "** is the winner!"
		
	def next(self):
		self.turnstate += 1
		if self.turnstate > 1: 
			self.turnstate = 0
			self.turn += 1
		
def handleMessage(message, prefix):
	txt = message.content
	if txt.startswith(prefix):
		if txt.lower().startswith(prefix + "challenge"):
			for battle in battles:
				if battle.isInBattle(message.author):
					return "You are already involved in a battle!"
			if len(message.mentions) > 0:
				battles.append(Battle(message.author,message.mentions[0],message.server,message.channel))
				return ":scales: **" + message.author.name + "** has challenged **" + message.mentions[0].name + "** to a battle! Type \"" + prefix + "accept\" to accept the challenge!\n**" + message.author.name + "** may \"" + prefix + "cancel\" the challenge before it is accepted."
			else:
				battles.append(Battle(message.author,None,message.server,message.channel))
				return ":loudspeaker: **" + message.author.name + "** has made an open challenge to anyone for a battle! Type \"" + prefix + "accept\" to answer the challenge!\n**" + message.author.name + "** may \"" + prefix + "cancel\" the challenge before it is accepted."
		if txt.lower().startswith(prefix + "battles"):
			retstr = ""
			if len(battles) > 0:
				for battle in battles:
					retstr += battle.status() + "\n"
				return retstr
			else:
				return "There are currently no battles. Type \"" + prefix + "challenge <@user_id>\" to challenge someone"
		if len(battles) > 0:
			i = 0
			for battle in battles:
				if txt.lower().startswith(prefix + "accept"):
					if not battle.challengee.user or message.author == battle.challengee.user:
						if not battle.challengee.user: 
							battle.challengee.user = message.author
						battle.state = "Choosing Loadouts"
						return "**" + battle.challenger.user.name + "** vs. **" + battle.challengee.user.name + "**\nThe Battle Is About To Begin!\n*TIP: At any time you can use \"" + prefix + "status\" to see the battle information.*\n\n" + battle.options(prefix)
				if txt.lower().startswith(prefix + "decline"):
					if message.author == battle.challengee.user:
						if battle.state == "Awaiting Opponent":
							del battles[i]
							return ":broken_heart: **" + message.author.name + "** has declined the challenge!"
				if txt.lower().startswith(prefix + "cancel"):
					if message.author == battle.challenger.user:
						if battle.state == "Awaiting Opponent":
							del battles[i]
							return ":x: **" + message.author.name + "** has canceled his challenge!"
				###################################
				# All actual in battle stuff here #
				###################################
				if battle.isInBattle(message.author):
					### forfeit
					if txt.lower().startswith(prefix + "forfeit"):
						retstr = battle.forfeit(message.author)
						del battles[i]
						return retstr
					### status   
					if txt.lower().startswith(prefix + "status"):
						retstr = battle.status()
						if battle.isPlayersTurn(message.author):
							retstr += "\n\n" + battle.options(prefix)
						return retstr
					### options
					if txt.lower().startswith(prefix + "options"):
						if battle.isPlayersTurn(message.author):
							return battle.options(prefix)
						else:
							return ":warning: It is currently not your turn, please wait..."
					### choosing loadouts
					if battle.state == "Choosing Loadouts":
						retstr = ""
						if txt.lower().startswith(prefix + "warrior"):
							retstr += battle.setClass(message.author,"warrior")
						if txt.lower().startswith(prefix + "wizard"):
							retstr += battle.setClass(message.author,"wizard")
						if txt.lower().startswith(prefix + "ranger"):
							retstr += battle.setClass(message.author,"ranger")
						if battle.challenger.battleclass and battle.challengee.battleclass:
							battle.turn = 1
							battle.state = "In Combat"
							retstr += "\nThe battle has begun! Rolling initiative!"
							battle.challenger.initiative = random.randint(1,20)
							battle.challengee.initiative = random.randint(1,20)
							retstr += "\n**" + battle.challenger.user.name + "** rolled " + str(battle.challenger.initiative) + "(+" + str(battle.challenger.dexterity) + ") | **" + battle.challengee.user.name + "** rolled " + str(battle.challengee.initiative) + "(+" + str(battle.challengee.dexterity) + ")"
							if battle.challenger.initiative + battle.challenger.dexterity > battle.challengee.initiative + battle.challengee.dexterity:
								battle.challengerGoesFirst = True
							else:
								battle.challengerGoesFirst = False
							retstr += "\n\n" + battle.options(prefix)
						return retstr
					### in combat
					if battle.state == "In Combat":
						if txt.lower().startswith(prefix + "attack"):
							if battle.isPlayersTurn(message.author):
								retstr = battle.attack(message.author)
								if battle.isOpponentDead(message.author):
									retstr += "\n\n:skull: **"
									if message.author == battle.challenger.user:
										retstr += battle.challengee.user.name
									else:
										retstr += battle.challenger.user.name
									retstr += "** is dead!\n:trophy: **" + message.author.name + "** is the winner!"
									del battles[i]
								else:
									retstr += "\n" + battle.status() + "\n\n" + battle.options(prefix)
								return retstr
						
						if txt.lower().startswith(prefix + "abilities"):
							if battle.isPlayersTurn(message.author):
								return battle.abilities(message.author, prefix)
							
						if txt.lower().startswith(prefix + "run"):
							if battle.isPlayersTurn(message.author):
								retstr = battle.run(message.author)
								del battles[i]
								return retstr
						# Abilities
						if txt.lower().startswith(prefix + "heal"):
							if battle.isPlayersTurn(message.author):
							# allow for healing teammates or "all"
								return battle.heal(message.author) + "\n\n" + battle.status() + "\n" + battle.options(prefix)
						
						if txt.lower().startswith(prefix + "Energy Bolt"):
							if battle.isPlayersTurn(message.author):
								return battle.heal(message.author) + "\n\n" + battle.status() + "\n" + battle.options(prefix)
						
						
				i += 1
	return ""
