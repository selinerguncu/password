global conn
global cur
global session
global appPath

import sys
import web
import sqlite3 as sqlite
import base64

appPath = "/Users/selinerguncu/Desktop/PythonProjects/Fun Projects/TestGame"
templatePath = appPath + '/templates'
# to be able to import local modules
sys.path.append(appPath)

from numberGame import code
from utils.parseFormData import parseFormData
from utils.getSession import getSession
from utils.errors import errors




web.config.debug = False
web.config.session_parameters['cookie_name'] = 'session_id'


urls = (
	'/', 'Login',
	'/intro', 'Intro',
	'/howtoplay', 'HowToPlay',
	'/setup', 'Setup',
	'/game', 'Game',
	'/guesses', 'Guesses',
	'/end', 'End'
)

app = web.application(urls, globals())
render = web.template.render(templatePath)
db = web.database(dbn='sqlite', db = appPath + '/data/gamedb.sqlite', check_same_thread=False)
store = web.session.DBStore(db, 'sessions')
session = web.session.Session(app, store, initializer={'player_id':'guest', 'game_id': 0})


class Intro():
	def GET(self):
		print 'username in intro', activeSession['username']
		return render.intro()


class HowToPlay():
	def GET(self):
		return render.howtoplay()


class Login():
	def GET(self):
		if session.player_id == 'guest':
			return render.login()
		else:
			return web.seeother('/setup')

	def POST(self):

		conn = sqlite.connect(appPath + '/data/gamedb.sqlite')
		cur = conn.cursor()
		data = parseFormData(web.data())
		form_username = data["username"]
		form_userPassword = data["userpassword"]

		cur.execute('''SELECT userpassword, id FROM Player WHERE username = ?''', (form_username,))
		pass_and_id = cur.fetchone()

		if pass_and_id != None:
			db_userPassword = pass_and_id[0]
			player_id = pass_and_id[1]

			if db_userPassword == form_userPassword:
				session.player_id = player_id
				return web.seeother('/setup')
			else:
				return render.login(errors["password"])

		else:
			cur.execute('''INSERT INTO Player(username, userpassword) VALUES (?, ?)''', (form_username, form_userPassword))
			conn.commit()
			session.player_id = cur.lastrowid
			return web.seeother('/setup')


class Setup(object):
	def GET(self):
		if session.player_id == 'guest':
			return web.seeother('/')

		if session.game_id == 0:
			return render.setup()
		else:
			return web.seeother('/game')

	def POST(self):
		data = parseFormData(web.data())
		conn = sqlite.connect(appPath + '/data/gamedb.sqlite')
		cur = conn.cursor()

		error = self.validate(data)
		warning = self.hasWarning(data)

		if (error == None and warning == None) or (error == None and int(data["force"]) == 1):
			cur.execute('''
				INSERT INTO Game(digits, complexity, goldCoins, silverCoins, player_id) 
				VALUES (?, ?, ?, ?, ?)
				''', (data["digits"], data["complexity"], data["goldCoins"], data["silverCoins"], session.player_id))
			conn.commit()
			session.game_id = cur.lastrowid
			return web.seeother('/game')
						
		elif error == None and warning != None:
			return render.setup(errors[warning], data)
		else:
			return render.setup(errors[error], data, True)

	def hasWarning(self, data):
		warning = None
		
		if int(data["goldCoins"]) > 100 or int(data["silverCoins"]) > 100:
			warning = "max100"
		elif int(data["goldCoins"]) < 20 or int(data["silverCoins"]) < 20:
			warning = "min20"
		else:
			if int(data["goldCoins"]) < 50 and int(data["complexity"]) == 1:
				warning = "gold50complex"
			elif int(data["goldCoins"]) < 70 and int(data["complexity"]) == 2:
				warning = "gold70complex"
			if int(data["goldCoins"]) < 30 and int(data["digits"]) == 4:
				warning = "gold30"
			elif int(data["goldCoins"]) < 30 and int(data["digits"]) == 5:
				warning = "gold30"
			elif int(data["goldCoins"]) < 40 and int(data["digits"]) == 6:
				warning = "gold40"
			elif int(data["goldCoins"]) < 50 and int(data["digits"]) == 7:
				warning = "gold50"
			elif int(data["goldCoins"]) < 60 and int(data["digits"]) == 8:
				warning = "gold60"
			elif int(data["silverCoins"]) < 50 and int(data["complexity"]) == 1:
				warning = "silver50complex"
			elif int(data["silverCoins"]) < 70 and int(data["complexity"]) == 2:
				warning = "silver70complex"
			elif int(data["silverCoins"]) < 30 and int(data["digits"]) == 4:
				warning = "silver30"
			elif int(data["silverCoins"]) < 30 and int(data["digits"]) == 5:
				warning = "silver30"
			elif int(data["silverCoins"]) < 40 and int(data["digits"]) == 6:
				warning = "silver40"
			elif int(data["silverCoins"]) < 50 and int(data["digits"]) == 7:
				warning = "silver50"
			elif int(data["silverCoins"]) < 60 and int(data["digits"]) == 8:
				warning = "silver60"

		return warning


	def validate(self, data):
		
		err = None

		if data["goldCoins"] == "" and data["silverCoins"] != "":
			err = "goldAmount"
		elif data["silverCoins"] == "" and data["goldCoins"] != "":
			err = "silverAmount"
		elif data["silverCoins"] == "" and data["goldCoins"] == "":
			err = "goldSilverAmount"
		
		return err

	
class Game(object):
	def __init__(self):
		self.a = code.Password(activeSession["setup"]["digits"], activeSession["setup"]["complexity"], activeSession["setup"]["goldCoins"], activeSession["setup"]["silverCoins"])
		print 'activeSession["setup"]["digits"]', activeSession["setup"]["digits"]

		print 'activeSession["setup"]', activeSession["setup"]


	def GET(self):
		# conn = sqlite.connect(appPath + '/data/gamedb.sqlite')
		# cur = conn.cursor()
		
		# cur.execute('''SELECT id FROM Game WHERE player_id = ?''', (session.player_id,))
		# game_id = cur.fetchone()

		# if game_id != None:
		# 	return web.seeother('/guesses')
		# else:
		# 	return render.setup()

		session.password = self.a.create()
		activeSession["password"] = session.password
		print 'is password?', session.password

		print 'GAME password 1', session.password
		print 'GAME password 1', activeSession["password"]
		return render.game(activeSession) 

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
		print 'GAME password3', activeSession["password"]

		# activeSession["pastGuess"] = guess
		# print "activeSession['pastGuess']", activeSession["pastGuess"]

		#check if all inputs are valid:

		onlyNumbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
		onlyLetters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'r', 's', 't', 'u', 'v', 'y', 'z', 'x', 'q', 'w']
		numbersLetters = onlyNumbers + onlyLetters
		
		if activeSession["setup"]["complexity"] == '0' and len(guess) > len(set(guess)):
			return render.game(activeSession, errors["uniqueNumbers"])
		elif activeSession["setup"]["complexity"] == '1' and len(guess) > len(set(guess)):
			return render.game(activeSession, errors["uniqueLetters"])
		elif activeSession["setup"]["complexity"] == '2' and len(guess) > len(set(guess)):
			return render.game(activeSession, errors["uniqueNumbersLetters"])
		elif activeSession["setup"]["complexity"] == '0' and len([1 for i in guess if i in onlyNumbers]) != int(activeSession["setup"]["digits"]):
			return render.game(activeSession, errors["onlyNumbers"])
		elif activeSession["setup"]["complexity"] == '1' and len([1 for i in guess if i in onlyLetters]) != int(activeSession["setup"]["digits"]):
			return render.game(activeSession, errors["onlyLetters"])
		elif activeSession["setup"]["complexity"] == '2' and len([1 for i in guess if i in numbersLetters]) != int(activeSession["setup"]["digits"]):
			return render.game(activeSession, errors["numbersLetters"])
		else:
			activeSession["round"] = 0
			self.evaluation = self.a.evaluate(activeSession["password"], guess)
			self.updated = self.a.update(activeSession["setup"]["goldCoins"], activeSession["setup"]["silverCoins"], activeSession["round"], self.evaluation)

			session.evaluation = self.evaluation
			activeSession["evaluation"] = session.evaluation
			session.updated = self.updated
			activeSession["updated"] = session.updated

			print "before activeSession['round']", activeSession["round"]

			activeSession["round"] = activeSession["updated"]["round"]

			print "after activeSession['round']", activeSession["round"]

			# print 'evaluation', session.evaluation
			# print 'guess', session.updated["guess"]

			if activeSession["updated"]["guess"] == activeSession["password"]:
				return web.seeother('/end')
			else:
				temp = {}
				temp["guess"] = activeSession["updated"]["guess"]
				activeSession["round"] = activeSession["updated"]["round"]
				temp["goldCoinsReceived"] = activeSession["updated"]["goldCoinsReceived"]
				temp["silverCoinsReceived"] = activeSession["updated"]["silverCoinsReceived"]
				activeSession["setup"]["goldCoins"] = activeSession["updated"]["goldCoinsInBag"]
				activeSession["setup"]["silverCoins"] = activeSession["updated"]["silverCoinsInBag"]
				activeSession["updated"] = self.a.update(activeSession["setup"]["goldCoins"], activeSession["setup"]["silverCoins"], activeSession["round"], temp)
				
				#recording previous guesses in the list:
				# session.pastRound.append(activeSession["updated"]["round"])
				# session.pastGuess.append(temp["guess"])
				# session.pastGold.append(temp["goldCoinsReceived"])
				# session.pastSilver.append(temp["silverCoinsReceived"])

				# print "activeSession['pastGuess']", activeSession["pastGuess"]
				# print "(temp['guess'])", (temp["guess"])

				activeSession["pastRound"].append(activeSession["updated"]["round"])
				activeSession["pastGuess"].append(temp["guess"])
				activeSession["pastGold"].append(temp["goldCoinsReceived"])
				activeSession["pastSilver"].append(temp["silverCoinsReceived"])
				
				activeSession["past"] = zip(activeSession["pastRound"], activeSession["pastGuess"], activeSession["pastGold"], activeSession["pastSilver"])

				# print 'ilk round', activeSession["updated"]["round"]
				# print 'session daki ilk round', session.pastRound
				print len([1 for i in guess if i in onlyNumbers])
				print int(activeSession["setup"]["digits"])
				return web.seeother('/guesses')
				# render.guesses(session)


class Guesses(object):
	def __init__(self):
		self.a = code.Password(activeSession["setup"]["digits"], activeSession["setup"]["complexity"], activeSession["setup"]["goldCoins"], activeSession["setup"]["silverCoins"])

	def GET(self):
		return render.guesses(activeSession) 

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

		# activeSession["pastGuess"] = guess

		print 'len', len(guess)
		print 'set', set(guess)
		print 'lenSet', len(set(guess))
		
		#test if all inputs are valid:

		onlyNumbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
		onlyLetters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'r', 's', 't', 'u', 'v', 'y', 'z', 'x', 'q', 'w']
		numbersLetters = onlyNumbers + onlyLetters

		if activeSession["setup"]["complexity"] == '0' and len(guess) > len(set(guess)):
			return render.guesses(activeSession, errors["uniqueNumbers"])
		elif activeSession["setup"]["complexity"] == '1' and len(guess) > len(set(guess)):
			return render.guesses(activeSession, errors["uniqueLetters"])
		elif activeSession["setup"]["complexity"] == '2' and len(guess) > len(set(guess)):
			return render.guesses(activeSession, errors["uniqueNumbersLetters"])
		elif activeSession["setup"]["complexity"] == '0' and len([1 for i in guess if i in onlyNumbers]) != int(activeSession["setup"]["digits"]):
			return render.guesses(activeSession, errors["onlyNumbers"])
		elif activeSession["setup"]["complexity"] == '1' and len([1 for i in guess if i in onlyLetters]) != int(activeSession["setup"]["digits"]):
			return render.guesses(activeSession, errors["onlyLetters"])
		elif activeSession["setup"]["complexity"] == '2' and len([1 for i in guess if i in numbersLetters]) != int(activeSession["setup"]["digits"]):
			return render.guesses(activeSession, errors["numbersLetters"])
		else:
			self.evaluation = self.a.evaluate(activeSession["password"], guess)
			print "GUESS password", activeSession["password"]
			self.updated = self.a.update(activeSession["setup"]["goldCoins"], activeSession["setup"]["silverCoins"], activeSession["round"], self.evaluation)

			session.evaluation = self.evaluation
			activeSession["evaluation"] = session.evaluation		
			session.updated = self.updated
			activeSession["updated"] = session.updated

			activeSession["round"] = activeSession["updated"]["round"]

			print "after activeSession['round']", activeSession["round"]		

			if activeSession["updated"]["guess"] == activeSession["password"]:
				return web.seeother('/end')
			elif activeSession["updated"]["goldCoinsInBag"] == activeSession["updated"]["silverCoinsInBag"] == 0:
				return web.seeother('/end')

			else:
				print 'password', activeSession["password"]
				print 'evaluation', activeSession["evaluation"]
				print 'coins in bag', activeSession["updated"]["goldCoinsInBag"], activeSession["updated"]["silverCoinsInBag"]
				print 'updated', activeSession["updated"]
				temp = {}
				temp["guess"] = activeSession["updated"]["guess"]
				session.round = activeSession["updated"]["round"]
				temp["goldCoinsReceived"] = activeSession["updated"]["goldCoinsReceived"]
				temp["silverCoinsReceived"] = activeSession["updated"]["silverCoinsReceived"]
				activeSession["setup"]["goldCoins"] = activeSession["updated"]["goldCoinsInBag"]
				activeSession["setup"]["silverCoins"] = activeSession["updated"]["silverCoinsInBag"]
				activeSession["updated"] = self.a.update(activeSession["setup"]["goldCoins"], activeSession["setup"]["silverCoins"], activeSession["round"], temp)
				
				# #recording previous guesses in the list:
				# session.pastRound.append(activeSession["updated"]["round"])
				# session.pastGuess.append(temp["guess"])
				# session.pastGold.append(temp["goldCoinsReceived"])
				# session.pastSilver.append(temp["silverCoinsReceived"])


				activeSession["pastRound"].append(activeSession["updated"]["round"])
				activeSession["pastGuess"].append(temp["guess"])
				activeSession["pastGold"].append(temp["goldCoinsReceived"])
				activeSession["pastSilver"].append(temp["silverCoinsReceived"])

				
				activeSession["past"] = zip(activeSession["pastRound"], activeSession["pastGuess"], activeSession["pastGold"], activeSession["pastSilver"])

				return web.seeother('/guesses')


class End():
	def GET(self):
		conn = sqlite.connect(appPath + '/data/gamedb.sqlite')
		cur = conn.cursor()

		if activeSession["updated"]["guess"] == activeSession["password"]:
			# print "END password", session.password
			# print "session.pastGold", session.pastGold
			# print "session.pastSilver", session.pastSilver

			goldCoinsSpent = sum(activeSession["pastGold"])
			silverCoinsSpent = sum(activeSession["pastSilver"])

			print "session setup", activeSession["setup"]["goldCoins"], activeSession["setup"]["silverCoins"]
			print sum(activeSession["pastGold"]), sum(activeSession["pastSilver"])
			print "goldCoinsSpent", goldCoinsSpent
			print "silverCoinsSpent", silverCoinsSpent
			print "round", activeSession["updated"]["round"]

			self.score = code.Score(activeSession["setup"]["digits"], activeSession["setup"]["complexity"], goldCoinsSpent, silverCoinsSpent, activeSession["updated"]["round"])
			session.score = self.score.score()
			activeSession["score"] = session.score
			activeSession["gameOver"] = "won"
			print 'activeSession', activeSession
			#activeSession["setup"]["username"] = activeSession["username"]
			activeSession["goldCoinsSpent"] = goldCoinsSpent
			activeSession["silverCoinsSpent"] = silverCoinsSpent


		#writing from the database:
		#cur.execute("SELECT username, userpassword FROM Player")
		#row = cur.fetchone()
		#if row is None:
		#	pass
		#else:
		#	username, userpassword = row[0], row[1]
			cur.execute("SELECT id FROM Player WHERE username = (:username) ", activeSession)
			playerID = cur.fetchone()[0]
			print 'playerID', playerID

			cur.execute('''INSERT INTO Game(username, gameover, score, totalRounds, digits, complexity, goldSpent, silverSpent, player_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
				(activeSession["username"], activeSession["gameOver"], activeSession["score"], activeSession["round"],
					activeSession["setup"]["digits"], activeSession["setup"]["complexity"], activeSession["goldCoinsSpent"], activeSession["silverCoinsSpent"], playerID) )
			
			#cur.execute("UPDATE Game SET gameover = (:gameOver) WHERE username = (:username) ", activeSession)
			#cur.execute("UPDATE Game SET score = (:score) WHERE username = (:username) ", activeSession)
			#cur.execute("UPDATE Game SET totalRounds = (:round) WHERE username = (:username) ", activeSession)
			#cur.execute("UPDATE Game SET digits = (:digits) WHERE username = (:username) ", activeSession["setup"])
			#cur.execute("UPDATE Game SET complexity = (:complexity) WHERE username = (:username) ", activeSession["setup"])
			#cur.execute("UPDATE Game SET goldSpent = (:goldCoinsSpent) WHERE username = (:username) ", activeSession)
			#cur.execute("UPDATE Game SET silverSpent = (:silverCoinsSpent) WHERE username = (:username) ", activeSession)


			cur.execute("UPDATE Player SET wins = wins + 1 WHERE username = (:username) ", activeSession)
			cur.execute("UPDATE Player SET games = games + 1 WHERE username = (:username) ", activeSession)
			cur.execute("UPDATE Player SET totalScore = totalScore + (:score) WHERE username = (:username) ", activeSession)
			

			#maxScore in Player icin select yap: if maxScore > score: then update
			cur.execute("SELECT maxScore FROM Player WHERE username = (:username) ", activeSession)
			maxScore = cur.fetchone()
			if activeSession["score"] > maxScore:
				cur.execute("UPDATE Player SET maxScore = (:score) WHERE username = (:username) ", activeSession)
			else:
				cur.execute("UPDATE Player SET maxScore = maxScore WHERE username = (:username) ", activeSession)

			
			#if maxScore of a player is btw xxx and yyy then badge = diamond vs ruby vs sapphire vs emerald
			if activeSession["score"] >= 10000000000:
				activeSession["badge"] = 'Diamond'
			elif activeSession["score"] >= 1000000:
				activeSession["badge"] = 'Emerald'
			elif activeSession["score"] >= 100000:
				activeSession["badge"] = 'Sapphire'
			else:
				activeSession["badge"] = 'Ruby'
			
			print "score", activeSession["score"]
			print "badge", activeSession["badge"]

			cur.execute('''INSERT INTO Leaderboard(username, score, badge) VALUES (?, ?, ?)''', (activeSession["username"], activeSession["score"], activeSession["badge"]) )
			
			# if activeSession["score"] > 10000000000:
			# 	cur.execute("UPDATE Leaderboard SET badge = 'Diamond' WHERE username = (:username) ", activeSession)
			# elif activeSession["score"] > 1000000
			# 	cur.execute("UPDATE Leaderboard SET badge = 'Emerald' WHERE username = (:username) ", activeSession)
			# elif activeSession["score"] > 100000:
			# 	cur.execute("UPDATE Leaderboard SET badge = 'Sapphire' WHERE username = (:username) ", activeSession)
			# else:
			# 	cur.execute("UPDATE Leaderboard SET badge = 'Ruby' WHERE username = (:username) ", activeSession)


			conn.commit()
			return render.endwon(activeSession)

		elif activeSession["updated"]["goldCoinsInBag"] == activeSession["updated"]["silverCoinsInBag"] == 0:
			print 'coins in bag', activeSession["updated"]["goldCoinsInBag"], activeSession["updated"]["silverCoinsInBag"]
			
			activeSession["gameOver"] = "lost"
			activeSession["score"] = 0
			#activeSession["setup"]["username"] = activeSession["username"]

			cur.execute('''INSERT INTO Game(username, gameover, score, totalRounds, digits, complexity, goldSpent, silverSpent) VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', 
				(activeSession["username"], activeSession["gameOver"], activeSession["score"], activeSession["round"],
					activeSession["setup"]["digits"], activeSession["setup"]["complexity"], activeSession["setup"]["goldCoins"], activeSession["setup"]["silverCoins"] ) )
			
			cur.execute("UPDATE Player SET wins = wins + 1 WHERE username = (:username) ", activeSession)
			cur.execute("UPDATE Player SET games = games + 1 WHERE username = (:username) ", activeSession)
			cur.execute("UPDATE Player SET totalScore = totalScore + (:score) WHERE username = (:username) ", activeSession)
			
			#maxScore in Player icin select yap: if maxScore > score: then update
			cur.execute("SELECT maxScore FROM Player WHERE username = (:username) ", activeSession)
			if activeSession["score"] > maxScore:
				cur.execute("UPDATE Player SET maxScore = (:score) WHERE username = (:username) ", activeSession)
			else:
				cur.execute("UPDATE Player SET maxScore = ? WHERE username = ? ", (maxScore, activeSession["username"]))

			conn.commit()

			return render.endlost(activeSession)


if __name__ == "__main__":
	app.run()





 



