import json
import urllib.request

class Trends(object):
	

	def getGTrends(self, msg):
		try:
			token = "APP6_UEAAAAAWllTVOLUmeOUbACPKk0bM_hrWp1Mjhkv"
			topics = msg.split('"')
			if len(topics) > 3:
				# need to change date in url still
				url = "https://trends.google.com/trends/api/widgetdata/multiline/csv?req=%7B%22time%22%3A%222017-12-11%202018-01-11%22%2C%22resolution%22%3A%22DAY%22%2C%22locale%22%3A%22en-US%22%2C%22comparisonItem%22%3A%5B%7B%22geo%22%3A%7B%7D%2C%22complexKeywordsRestriction%22%3A%7B%22keyword%22%3A%5B%7B%22type%22%3A%22BROAD%22%2C%22value%22%3A%22" + topics[1] + "%22%7D%5D%7D%7D%2C%7B%22geo%22%3A%7B%7D%2C%22complexKeywordsRestriction%22%3A%7B%22keyword%22%3A%5B%7B%22type%22%3A%22BROAD%22%2C%22value%22%3A%22" + topics[3] + "%22%7D%5D%7D%7D%5D%2C%22requestOptions%22%3A%7B%22property%22%3A%22%22%2C%22backend%22%3A%22IZG%22%2C%22category%22%3A0%7D%7D&token=" + token + "&tz=300"
				try:
					rawtxt = urllib.request.urlopen(url).read()
				except:
					return "ERROR: Connection Not Established."
				#print(rawtxt)
				#rawtxt = "Category: All categories\n\nDay,justice league: (Worldwide),spiderman: (Worldwide)\n2017-12-11,54,50\n2017-12-12,48,50\n2017-12-13,46,46\n2017-12-14,50,46\n2017-12-15,56,48\n2017-12-16,77,59\n2017-12-17,74,59"
				c = 0
				t1 = 0
				t2 = 0
				for line in rawtxt.splitlines():
					if c > 3:
						data = line.split(",")
						try:
							t1 = t1 + int(data[1])
							t2 = t2 + int(data[2])
						except:
							print("Error: NaN")
					c = c + 1
				t1av = int(t1 / c)
				t2av = int(t2 / c)
				return "\"" + topics[1] + "\": " + str(t1av) + "   \"" + topics[3] + "\": " + str(t2av)
			
		except:
			return "mark is bad at scripting"
	
	def getToken():
		url = "tmp"

#print(Trends.getGTrends(object, ' "spiderman" "justice league"'))
#input("PRESS ENTER KEY TO EXIT")
#https://stackoverflow.com/questions/42317489/origin-of-tokens-in-google-trends-api-call
