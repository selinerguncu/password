import web
from numberGame import code

urls = (
	'/', 'Login',
	'/intro', 'Intro',
	'/howtoplay', 'HowToPlay',
	'/setup', 'Setup',
	'/sample2', 'Sample2',
	'/game', 'Game',
	'/guesses', 'Guesses',
	'/end', 'End'
)

app = web.application(urls, globals())

# Hack to make session play nice with the reloader (in debug mode)
if web.config.get('_session') is None:
    session = web.session.Session(app, web.session.DiskStore('sessions'))
    web.config._session = session
else:
    session = web.config._session


templatePath = '/Users/selinerguncu/Desktop/PythonProjects/Fun Projects/TestGame/templates'

render = web.template.render(templatePath)


def parseFormData(rawData):
	formData = rawData.split('&')
	data = {}
	
	for i in formData:
		param = i.split('=')
		data[param[0]] = param[1]

	return data

def listFormData(rawData):
	formData = rawData.split('&')
	data = []
	
	for i in formData:
		data.append(i)

	return data


class Login():
	def GET(self):
		print session.get("username")
		return render.login()

	def POST(self):
		data = parseFormData(web.data())
		session.username = data["username"]
		session.password = data["password"]
		print session.get("username")
		if data["username"] == "":
			return render.login("Please insert a valid username.")
		elif data["password"] == "":
			return render.login("Please create a valid password.")
		else:
			web.seeother("/intro")



class Intro():
	def GET(self):
		print session.get("username")
		return render.intro()


class HowToPlay():
	def GET(self):
		print session.get("username")
		return render.howtoplay()

	def POST(self):
		web.seeother('/')


class Sample2():
	def GET(self):
		return render.sample2()


class Setup(object):

	def GET(self):
		session.round = 0
		session.pastGuess = []
		session.pastGold = []
		session.pastSilver = []
		session.pastRound = []
		session.past = []

		print session.get("username")
		return render.setup()

	def POST(self):
		data = parseFormData(web.data())

		# verification:

		if data["goldCoins"] == "" and data["silverCoins"] != "":
			return render.setup("You have to have some amount of Gold coins in your bag.", data)
		elif data["silverCoins"] == "" and data["goldCoins"] != "":
			return render.setup("You have to have some amount of Silver coins in your bag.", data)
		elif data["silverCoins"] == "" and data["goldCoins"] == "":
			return render.setup("You have to have some amount of Gold and Silver coins in your bag.", data)
		else:
			if int(data["goldCoins"]) > 100 or int(data["silverCoins"]) > 100:
				session.setup = data
				return render.setup("You may wanto to set the the maximum number of Gold and Silver coins to be 100 for each bag. Otherwise, the game will be really easy.", data)
			elif int(data["goldCoins"]) < 20 or int(data["silverCoins"]) < 20:
				session.setup = data
				return render.setup("You may wanto to set the the minimum number of Gold and Silver coins to be 20 for each bag. Otherwise, the game will be really challenging.", data)
			

			if int(data["goldCoins"]) < 30 and int(data["digits"]) == 4:
				session.setup = data
				return render.setup("You may wanto to increase the number of Gold coins in your bag", data)
			elif int(data["goldCoins"]) < 30 and int(data["digits"]) == 5:
				session.setup = data
				return render.setup("You may wanto to increase the number of Gold coins in your bag", data)
			elif int(data["goldCoins"]) < 40 and int(data["digits"]) == 6:
				session.setup = data
				return render.setup("You may wanto to increase the number of Gold coins in your bag", data)
			elif int(data["goldCoins"]) < 50 and int(data["digits"]) == 7:
				session.setup = data
				return render.setup("You may wanto to increase the number of Gold coins in your bag", data)
			elif int(data["goldCoins"]) < 60 and int(data["digits"]) == 8:
				session.setup = data
				return render.setup("You may wanto to increase the number of Gold coins in your bag", data)
			elif int(data["goldCoins"]) < 30 and int(data["complexity"]) == 0:
				session.setup = data
				return render.setup("You may wanto to increase the number of Gold coins in your bag", data)
			elif int(data["goldCoins"]) < 50 and int(data["complexity"]) == 1:
				session.setup = data
				return render.setup("You may wanto to increase the number of Gold coins in your bag", data)
			elif int(data["goldCoins"]) < 70 and int(data["complexity"]) == 2:
				session.setup = data
				return render.setup("You may wanto to increase the number of Gold coins in your bag", data)
			elif int(data["silverCoins"]) < 30 and int(data["digits"]) == 4:
				session.setup = data
				return render.setup("You may wanto to increase the number of Silver coins in your bag", data)
			elif int(data["silverCoins"]) < 30 and int(data["digits"]) == 5:
				session.setup = data
				return render.setup("You may wanto to increase the number of Silver coins in your bag", data)
			elif int(data["silverCoins"]) < 40 and int(data["digits"]) == 6:
				session.setup = data
				return render.setup("You may wanto to increase the number of Silver coins in your bag", data)
			elif int(data["silverCoins"]) < 50 and int(data["digits"]) == 7:
				session.setup = data
				return render.setup("You may wanto to increase the number of Silver coins in your bag", data)
			elif int(data["silverCoins"]) < 60 and int(data["digits"]) == 8:
				session.setup = data
				return render.setup("You may wanto to increase the number of Silver coins in your bag", data)
			elif int(data["silverCoins"]) < 30 and int(data["complexity"]) == 0:
				session.setup = data
				return render.setup("You may wanto to increase the number of Silver coins in your bag", data)
			elif int(data["silverCoins"]) < 50 and int(data["complexity"]) == 1:
				session.setup = data
				return render.setup("You may wanto to increase the number of Silver coins in your bag", data)
			elif int(data["silverCoins"]) < 70 and int(data["complexity"]) == 2:
				session.setup = data
				return render.setup("You may wanto to increase the number of Silver coins in your bag", data)
			else:
				session.setup = data
				print session.setup
				return web.seeother("/game")
				
	
class Game(object):
	def __init__(self):
		self.a = code.Password(session.get("setup")["digits"], session.get("setup")["complexity"], session.get("setup")["goldCoins"], session.get("setup")["silverCoins"])
		session.password = self.a.create()
		# session.password = self.password

	def GET(self):
		# d = code.Password(session.get("setup")["digits"], session.get("setup")["complexity"]).length
		
		# c = code.Password(session.get("setup")["digits"], session.get("setup")["complexity"]).complexity

		# print code.Password.create(d, c)

		# return render.game(session.get("setup"))
		
		#numberGame.code.Password instance olarak cagirabilirsin template'da
		return render.game(session) 

		#return self.a.drawBoxes() ---> bu consola yapistiriyor

	def POST(self):
		data = parseFormData(web.data())
		guess = []

		guess.append(data["first"])
		guess.append(data["second"])
		guess.append(data["third"])
		guess.append(data["fourth"])
		try:
			guess.append(data["fifth"])
			guess.append(data["sixth"])
			guess.append(data["seventh"])
			guess.append(data["eighth"])
		except:
			pass

		#test if all inputs are valid:

		onlyNumbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
		onlyLetters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'r', 's', 't', 'u', 'v', 'y', 'z', 'x', 'q', 'w']
		numbersLetters = onlyNumbers + onlyLetters
		
		if len(guess) > len(set(guess)):
			return render.game(session, "All the inputs should be unique and digits should not be left blank. Please try again.")
		elif session.get("setup")["complexity"] == '0' and len([1 for i in guess if i in onlyNumbers]) != int(session.get("setup")["digits"]):
			return render.game(session, "Please use only numbers. Digits should not be left blank.")
		elif session.get("setup")["complexity"] == '1' and len([1 for i in guess if i in onlyLetters]) != int(session.get("setup")["digits"]):
			return render.game(session, "Please use only lower-case letters. Digits should not be left blank.")
		elif session.get("setup")["complexity"] == '2' and len([1 for i in guess if i in onlyLetters]) != int(session.get("setup")["digits"]):
			return render.game(session, "Please use only numbers or lower-case letters. Digits should not be left blank.")
		else:
			self.evaluation = self.a.evaluate(session.password, guess)
			self.updated = self.a.update(session.get("setup")["goldCoins"], session.get("setup")["silverCoins"], session.round, self.evaluation)

			session.evaluation = self.evaluation
			session.updated = self.updated
			# print 'password', session.password
			# print 'evaluation', session.evaluation
			# print 'guess', session.updated["guess"]


			if session.updated["guess"] == session.password:
				return render.end()
			else:
				temp = {}
				temp["guess"] = session.updated["guess"]
				session.round = session.updated["round"]
				temp["goldCoinsReceived"] = session.updated["goldCoinsReceived"]
				temp["silverCoinsReceived"] = session.updated["silverCoinsReceived"]
				session.get("setup")["goldCoins"] = session.updated["goldCoinsInBag"]
				session.get("setup")["silverCoins"] = session.updated["silverCoinsInBag"]
				session.updated = self.a.update(session.get("setup")["goldCoins"], session.get("setup")["silverCoins"], session.round, temp)
				
				#recording previous guesses in the list:
				session.pastRound.append(session.updated["round"])
				session.pastGuess.append(temp["guess"])
				session.pastGold.append(temp["goldCoinsReceived"])
				session.pastSilver.append(temp["silverCoinsReceived"])
				
				session.past = zip(session.pastRound, session.pastGuess, session.pastGold, session.pastSilver)

				# print 'ilk round', session.updated["round"]
				# print 'session daki ilk round', session.pastRound
				print len([1 for i in guess if i in onlyNumbers])
				print int(session.get("setup")["digits"])
				return web.seeother('/guesses')
				# render.guesses(session)


class Guesses(object):
	def __init__(self):
		self.a = code.Password(session.get("setup")["digits"], session.get("setup")["complexity"], session.get("setup")["goldCoins"], session.get("setup")["silverCoins"])

	def GET(self):
		return render.guesses(session) 

	def POST(self):
		data = parseFormData(web.data())
		guess = []

		guess.append(data["first"])
		guess.append(data["second"])
		guess.append(data["third"])
		guess.append(data["fourth"])
		try:
			guess.append(data["fifth"])
			guess.append(data["sixth"])
			guess.append(data["seventh"])
			guess.append(data["eighth"])
		except:
			pass

		print 'len', len(guess)
		print 'set', set(guess)
		print 'lenSet', len(set(guess))
		
		#test if all inputs are valid:

		onlyNumbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
		onlyLetters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'r', 's', 't', 'u', 'v', 'y', 'z', 'x', 'q', 'w']
		numbersLetters = onlyNumbers + onlyLetters

		if len(guess) > len(set(guess)):
			return render.guesses(session, "All the inputs should be unique and digits should not be left blank. Please try again.")
		elif session.get("setup")["complexity"] == '0' and len([1 for i in guess if i in onlyNumbers]) != int(session.get("setup")["digits"]):
			return render.guesses(session, "Please use only numbers. Digits should not be left blank.")
		elif session.get("setup")["complexity"] == '1' and len([1 for i in guess if i in onlyLetters]) != int(session.get("setup")["digits"]):
			return render.guesses(session, "Please use only lower-case letters. Digits should not be left blank.")
		elif session.get("setup")["complexity"] == '2' and len([1 for i in guess if i in onlyLetters]) != int(session.get("setup")["digits"]):
			return render.guesses(session, "Please use only numbers or lower-case letters. Digits should not be left blank.")
		else:
			self.evaluation = self.a.evaluate(session.password, guess)
			self.updated = self.a.update(session.get("setup")["goldCoins"], session.get("setup")["silverCoins"], session.round, self.evaluation)

			session.evaluation = self.evaluation			
			session.updated = self.updated


			if session.updated["guess"] == session.password:
				return web.seeother('/end')
			elif session.updated["goldCoinsInBag"] == session.updated["silverCoinsInBag"] == 0:
				return web.seeother('/end')

			else:
				print 'password', session.password
				print 'evaluation', session.evaluation
				print 'coins in bag', session.updated["goldCoinsInBag"], session.updated["silverCoinsInBag"]
				print 'update', session.updated
				temp = {}
				temp["guess"] = session.updated["guess"]
				session.round = session.updated["round"]
				temp["goldCoinsReceived"] = session.updated["goldCoinsReceived"]
				temp["silverCoinsReceived"] = session.updated["silverCoinsReceived"]
				session.get("setup")["goldCoins"] = session.updated["goldCoinsInBag"]
				session.get("setup")["silverCoins"] = session.updated["silverCoinsInBag"]
				session.updated = self.a.update(session.get("setup")["goldCoins"], session.get("setup")["silverCoins"], session.round, temp)
				
				#recording previous guesses in the list:
				session.pastRound.append(session.updated["round"])
				session.pastGuess.append(temp["guess"])
				session.pastGold.append(temp["goldCoinsReceived"])
				session.pastSilver.append(temp["silverCoinsReceived"])
				
				session.past = zip(session.pastRound, session.pastGuess, session.pastGold, session.pastSilver)


				return web.seeother('/guesses')


class End():
	def GET(self):
		if session.updated["guess"] == session.password:
			session.kill()
			return render.endwon(session)
		elif session.updated["goldCoinsInBag"] == session.updated["silverCoinsInBag"] == 0:
			print 'coins in bag', session.updated["goldCoinsInBag"], session.updated["silverCoinsInBag"]
			session.kill()
			return render.endlost(session)














if __name__ == "__main__":
	app.run()
