import sys
global appPath
appPath = "/Users/selinerguncu/Desktop/PythonProjects/Fun Projects/TestGame"

sys.path.append(appPath)

import web
import sqlite3 as sqlite
import base64

from numberGame import code
from utils.parseFormData import parseFormData
from utils.getSession import getSession
from utils.errors import errors

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

global activeSession
global conn
global cur
global session

app = web.application(urls, globals())

templatePath = appPath + '/templates'
render = web.template.render(templatePath)

# if web.config.get('_session') is None:
#     session = web.session.Session(app, web.session.DBStore('sessions'))
#     web.config._session = session
# else:
#     session = web.config._session


web.config.session_parameters['cookie_name'] = 'session_id'
db = web.database(dbn='sqlite', db = appPath + '/data/gamedb.sqlite', check_same_thread=False)
store = web.session.DBStore(db, 'sessions')
session = web.session.Session(app, store, initializer={'player_id':'guest'})
# print session


activeSession = {}
conn = sqlite.connect(appPath + '/data/gamedb.sqlite')



class Login():
	def GET(self):
		session_id = web.cookies()["session_id"]
		conn = sqlite.connect(appPath + '/data/gamedb.sqlite')
		cur = conn.cursor()
		cur.execute('''SELECT data FROM sessions WHERE session_id = (?)''', (session_id,))
		session_data = web.session.Store.decode(store, cur.fetchone()[0])

		# print session_data["player_id"], session_data["session_id"]
		return render.login()

	def POST(self):
		data = parseFormData(web.data())

		conn = sqlite.connect(appPath + '/data/gamedb.sqlite')
		cur = conn.cursor()

		session.username = data["username"]
		session.userpassword = data["userpassword"]
		
		activeSession["username"] = session.username
		activeSession["userpassword"] = session.userpassword
		print 'is?', session.username

		cur.execute('''INSERT INTO Player(username, userpassword) VALUES (:username, :userpassword)''', activeSession)
		conn.commit()
		# vars = dict(username=activeSession['username'])
		# db.insert('Player', username=vars)


		#cur.execute (''' INSERT INTO Player(username) VALUES (?) ''' , activeSession['username'])
		#conn.commit()


		print 'app', session.get("username")
		print 'session.username', session.username
		print 'session.userpassword', session.userpassword
		
		if data["username"] == "":
			return render.login(errors["username"])
		elif data["userpassword"] == "":
			return render.login(errors["password"])
		else:
			web.seeother("/intro")


class Intro():
	def GET(self):
		print 'username in intro', activeSession['username']
		return render.intro()


class HowToPlay():
	def GET(self):
		return render.howtoplay()


class Sample2():
	def GET(self):
		return render.sample2()


class Setup(object):
	def GET(self):
		# if "round" in activeSession.keys():
		# 	del activeSession["pastGuess"]
		# 	del activeSession["updated"]
		# 	del activeSession["setup"]
		# 	del activeSession["pastSilver"]
		# 	del activeSession["pastGold"]
		# 	del activeSession["pastRound"]
		# 	del activeSession["past"]
		# 	del activeSession["score"]
		# 	del activeSession["password"]
		# 	del activeSession["evaluation"]
		# 	del activeSession["round"]
		# else:
		
		activeSession["pastGuess"] = []
		activeSession["pastGold"] = []
		activeSession["pastSilver"] = []
		activeSession["pastRound"] = []
		activeSession["past"] = []

		# session.pastGuess = []
		# session.pastGold = []
		# session.pastSilver = []
		# session.pastRound = []
		# session.past = []

		print 'username in setup', activeSession['username']
		print 'userpassword in setup', activeSession['userpassword']
		return render.setup()

	def POST(self):
		data = parseFormData(web.data())
		print 'data parsed', data

		# verification:

		if data["goldCoins"] == "" and data["silverCoins"] != "":
			return render.setup(errors["goldAmount"], data)
		elif data["silverCoins"] == "" and data["goldCoins"] != "":
			return render.setup(errors["silverAmount"], data)
		elif data["silverCoins"] == "" and data["goldCoins"] == "":
			return render.setup(errors["goldSilverAmount"], data)
		elif int(data["goldCoins"]) > 100 or int(data["silverCoins"]) > 100:
			session.setup = data
			activeSession["setup"] = session.setup
			return render.setup(errors["max100"], data)
		elif int(data["goldCoins"]) < 20 or int(data["silverCoins"]) < 20:
			session.setup = data
			activeSession["setup"] = session.setup
			return render.setup(errors["min20"], data)
		else:
			# if int(data["goldCoins"]) < 30 and int(data["complexity"]) == 0:
			# 	session.setup = data
			# 	return render.setup(errors.gold30complex, data)
			if int(data["goldCoins"]) < 50 and int(data["complexity"]) == 1:
				session.setup = data
				activeSession["setup"] = session.setup
				return render.setup(errors["gold50complex"], data)
			elif int(data["goldCoins"]) < 70 and int(data["complexity"]) == 2:
				session.setup = data
				activeSession["setup"] = session.setup
				return render.setup(errors["gold70complex"], data)
			if int(data["goldCoins"]) < 30 and int(data["digits"]) == 4:
				session.setup = data
				activeSession["setup"] = session.setup
				return render.setup(errors["gold30"], data)
			elif int(data["goldCoins"]) < 30 and int(data["digits"]) == 5:
				session.setup = data
				activeSession["setup"] = session.setup
				return render.setup(errors["gold30"], data)
			elif int(data["goldCoins"]) < 40 and int(data["digits"]) == 6:
				session.setup = data
				activeSession["setup"] = session.setup
				return render.setup(errors["gold40"], data)
			elif int(data["goldCoins"]) < 50 and int(data["digits"]) == 7:
				session.setup = data
				activeSession["setup"] = session.setup
				return render.setup(errors["gold50"], data)
			elif int(data["goldCoins"]) < 60 and int(data["digits"]) == 8:
				session.setup = data
				activeSession["setup"] = session.setup
				return render.setup(errors["gold60"], data)
			# elif int(data["silverCoins"]) < 30 and int(data["complexity"]) == 0:
			# 	session.setup = data
			# 	return render.setup("You may wanto to increase the number of Silver coins in your bag", data)
			elif int(data["silverCoins"]) < 50 and int(data["complexity"]) == 1:
				session.setup = data
				activeSession["setup"] = session.setup
				return render.setup(errors["silver50complex"], data)
			elif int(data["silverCoins"]) < 70 and int(data["complexity"]) == 2:
				session.setup = data
				activeSession["setup"] = session.setup
				return render.setup(errors["silver70complex"], data)
			elif int(data["silverCoins"]) < 30 and int(data["digits"]) == 4:
				session.setup = data
				activeSession["setup"] = session.setup
				return render.setup(errors["silver30"], data)
			elif int(data["silverCoins"]) < 30 and int(data["digits"]) == 5:
				session.setup = data
				activeSession["setup"] = session.setup
				return render.setup(errors["silver30"], data)
			elif int(data["silverCoins"]) < 40 and int(data["digits"]) == 6:
				session.setup = data
				activeSession["setup"] = session.setup
				return render.setup(errors["silver40"], data)
			elif int(data["silverCoins"]) < 50 and int(data["digits"]) == 7:
				session.setup = data
				activeSession["setup"] = session.setup
				return render.setup(errors["silver50"], data)
			elif int(data["silverCoins"]) < 60 and int(data["digits"]) == 8:
				session.setup = data
				activeSession["setup"] = session.setup
				return render.setup(errors["silver60"], data)
			else:
				session.setup = data
				activeSession["setup"] = session.setup

				print 'is setup?', session.setup

				print 'activeSession["setup"]', activeSession["setup"]
				print 'activeSession["username"]', activeSession["username"]
				print 'activeSession["setup"]["digits"]', activeSession["setup"]["digits"]
				return web.seeother("/game")

	
class Game(object):
	def __init__(self):
		self.a = code.Password(activeSession["setup"]["digits"], activeSession["setup"]["complexity"], activeSession["setup"]["goldCoins"], activeSession["setup"]["silverCoins"])
		print 'activeSession["setup"]["digits"]', activeSession["setup"]["digits"]

		print 'activeSession["setup"]', activeSession["setup"]


	def GET(self):
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
				cur.execute("UPDATE Player SET maxScore = maxScore WHERE username = (:username) ", activeSession)

			conn.commit()

			return render.endlost(activeSession)


if __name__ == "__main__":
	app.run()





 



