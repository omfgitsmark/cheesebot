import random


class Deck(object):
	current = 0
	cards = [{'value': 2, 'suit': 'spades'}, {'value': 3, 'suit': 'spades'}, {'value': 4, 'suit': 'spades'}, {'value': 5, 'suit': 'spades'}, {'value': 6, 'suit': 'spades'}, {'value': 7, 'suit': 'spades'}, {'value': 8, 'suit': 'spades'}, {'value': 9, 'suit': 'spades'}, {'value': 10, 'suit': 'spades'}, {'value': 11, 'suit': 'spades'}, {'value': 12, 'suit': 'spades'}, {'value': 13, 'suit': 'spades'}, {'value': 14, 'suit': 'spades'}, {'value': 2, 'suit': 'clubs'}, {'value': 3, 'suit': 'clubs'}, {'value': 4, 'suit': 'clubs'}, {'value': 5, 'suit': 'clubs'}, {'value': 6, 'suit': 'clubs'}, {'value': 7, 'suit': 'clubs'}, {'value': 8, 'suit': 'clubs'}, {'value': 9, 'suit': 'clubs'}, {'value': 10, 'suit': 'clubs'}, {'value': 11, 'suit': 'clubs'}, {'value': 12, 'suit': 'clubs'}, {'value': 13, 'suit': 'clubs'}, {'value': 14, 'suit': 'clubs'}, {'value': 2, 'suit': 'hearts'}, {'value': 3, 'suit': 'hearts'}, {'value': 4, 'suit': 'hearts'}, {'value': 5, 'suit': 'hearts'}, {'value': 6, 'suit': 'hearts'}, {'value': 7, 'suit': 'hearts'}, {'value': 8, 'suit': 'hearts'}, {'value': 9, 'suit': 'hearts'}, {'value': 10, 'suit': 'hearts'}, {'value': 11, 'suit': 'hearts'}, {'value': 12, 'suit': 'hearts'}, {'value': 13, 'suit': 'hearts'}, {'value': 14, 'suit': 'hearts'}, {'value': 2, 'suit': 'diamonds'}, {'value': 3, 'suit': 'diamonds'}, {'value': 4, 'suit': 'diamonds'}, {'value': 5, 'suit': 'diamonds'}, {'value': 6, 'suit': 'diamonds'}, {'value': 7, 'suit': 'diamonds'}, {'value': 8, 'suit': 'diamonds'}, {'value': 9, 'suit': 'diamonds'}, {'value': 10, 'suit': 'diamonds'}, {'value': 11, 'suit': 'diamonds'}, {'value': 12, 'suit': 'diamonds'}, {'value': 13, 'suit': 'diamonds'}, {'value': 14, 'suit': 'diamonds'}]
	
	def __init__(self):
		random.shuffle(self.cards)
		self.current = 0
		
	def shuffle(self):
		random.shuffle(self.cards)
		self.current = 0
		
	def deal(self, amount=1):
		retarr = []
		if self.remaining() < amount:
			self.shuffle()
		for i in range(0, amount):
			retarr.append(self.cards[self.current])
			self.current += 1
			if self.current >= 52:
				self.shuffle()
		return retarr
	
	def remaining(self):
		return len(self.cards) - self.current
		
	def burn(self, amount=1):
		self.current += amount
	
	def toString(self, cards):
		retstr = ""
		for card in cards:
			retstr += ":" + card['suit'] + ": "
			if card['value'] > 10:
				if card['value'] == 11: retstr += "J".ljust(4)
				if card['value'] == 12: retstr += "Q".ljust(4)
				if card['value'] == 13: retstr += "K".ljust(4)
				if card['value'] == 14: retstr += "A".ljust(4)
			else:
				retstr += str(card['value']).ljust(4)
		return retstr
		

deck = Deck()