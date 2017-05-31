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
	'/login', 'Login',
	'/intro', 'Intro',
	'/howtoplay', 'HowToPlay',
	'/setup', 'Setup',
	'/game', 'Game',
	'/guesses', 'Guesses',
	'/gameover', 'GameOver'
)

app = web.application(urls, globals())
render = web.template.render(templatePath, base='layout')
db = web.database(dbn='sqlite', db = appPath + '/data/gamedb.sqlite', check_same_thread=False)
store = web.session.DBStore(db, 'sessions')
session = web.session.Session(app, store, initializer={'player_id':'guest', 'game_id': 0})

def rowToDict(cur, row):
	d = {}
	for index, description in enumerate(cur.description):
		d[description[0]] = row[index]

	return d


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
			conn = sqlite.connect(appPath + '/data/gamedb.sqlite')
			cur = conn.cursor()
			cur.execute('''SELECT Leaderboard.score, Leaderboard.badge, Player.username 
				FROM Leaderboard JOIN Player ON Leaderboard.player_id = Player.id 
				ORDER BY Leaderboard.score DESC LIMIT 5''')
			leaders = cur.fetchall()

			return render.login(leaders)
		else:
			return web.seeother('/game')


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
				return web.seeother('/game')
			else:
				return render.login(errors["password"])

		else:
			cur.execute('''INSERT INTO Player(username, userpassword) VALUES (?, ?)''', (form_username, form_userPassword))
			conn.commit()
			session.player_id = cur.lastrowid
			return web.seeother('/game')


class Profile():
	def GET(self):
		player = {}
		player["username"] = 'sinan'
		player["games"] = 3
		player["difficulty"] = ['Easy', 'Mod', 'Hard']
		player["totalBadges"] = [38, 12, 2]
		player["badgeType"] = ['Ruby', 'Ruby', 'Emerald']
		player["totalScore"] = [1234, 4567, 9870]
		player["maxScore"] = [456, 1234, 643]
		player["stages"] = [10, 8, 2]
		player["level"] = [5, 4, 3]

		return render.profile(player)

	def POST(self):

		print web.data()
		return web.data()

		

class Setup(object):
	def GET(self):
		if session.player_id == 'guest':
			return web.seeother('/')

		if session.game_id == 0:
			return render.setup()
		else:
			conn = sqlite.connect(appPath + '/data/gamedb.sqlite')
			cur = conn.cursor()
			cur.execute('''SELECT won FROM Game WHERE id = ?''', (session.game_id,))
			gameRow = cur.fetchone()
			
			if gameRow[0] in [0, 1]:
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
		self.count = 0
		conn = sqlite.connect(appPath + '/data/gamedb.sqlite')
		cur = conn.cursor()
		game_id = session.game_id
		cur.execute('''SELECT * FROM Game WHERE id = ?''', (game_id,))
		gameRow = cur.fetchone()

		if gameRow == None:
			return

		self.game = rowToDict(cur, gameRow)
		self.password = code.Password(self.game["digits"], self.game["complexity"], self.game["goldCoins"], self.game["silverCoins"])

		self.password.drawBoxes()
		
		if self.game["password"] == None:
			password = ''.join(self.password.create())
			cur.execute("UPDATE Game SET password = ? WHERE id = ? ", (password, game_id))
			conn.commit()
			self.game["password"] = password

	def writeHistory(self, evaluation):
		print evaluation
		conn = sqlite.connect(appPath + '/data/gamedb.sqlite')
		cur = conn.cursor()
		cur.execute('''
			INSERT INTO History(round, guess, goldReceived, silverReceived, goldInBag, silverInBag, game_id)
			VALUES (?, ?, ?, ?, ?, ?, ?)'''
			, (evaluation["_round"], ''.join(evaluation["guess"]), evaluation["goldCoinsReceived"], evaluation["silverCoinsReceived"], evaluation["goldInBag"], evaluation["silverInBag"], session.game_id))
		conn.commit()


	def GET(self):

		if session.player_id == 'guest':
			return web.seeother('/')

		if session.game_id == '0':
			return web.seeother('/setup')

		conn = sqlite.connect(appPath + '/data/gamedb.sqlite')
		cur = conn.cursor()
		
		cur.execute('''SELECT round, guess, goldReceived, silverReceived, goldInBag, silverInBag FROM History WHERE game_id = ?''', (session.game_id,))
		history = cur.fetchall()

		past = []
		for row in history:
			past.append(row)

		return render.game(self.game, past) 


	def POST(self):
		data = parseFormData(web.data())
		guess = [data["first"], data["second"], data["third"], data["fourth"]]

		try:
			guess.append(data["fifth"])
			guess.append(data["sixth"])
			guess.append(data["seventh"])
			guess.append(data["eighth"])
		except:
			pass

		#check if all inputs are valid:

		onlyNumbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
		onlyLetters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'r', 's', 't', 'u', 'v', 'y', 'z', 'x', 'q', 'w']
		numbersLetters = onlyNumbers + onlyLetters

		conn = sqlite.connect(appPath + '/data/gamedb.sqlite')
		cur = conn.cursor()
		cur.execute("SELECT goldInBag, silverInBag, round, guess, goldReceived, silverReceived FROM History WHERE game_id = ?", (session.game_id,))
		rows = cur.fetchall()

		past = []
		for row in rows:
			past.append((row[2], row[3], row[4], row[5], row[0], row[1]))
		
		if self.game["complexity"] == 0 and len(guess) > len(set(guess)):
			return render.game(self.game, past, errors["uniqueNumbers"])
		elif self.game["complexity"] == 1 and len(guess) > len(set(guess)):
			return render.game(self.game, past, errors["uniqueLetters"])
		elif self.game["complexity"] == 2 and len(guess) > len(set(guess)):
			return render.game(self.game, past, errors["uniqueNumbersLetters"])
		elif self.game["complexity"] == 0 and len([1 for i in guess if i in onlyNumbers]) != int(self.game["digits"]):
			return render.game(self.game, past, errors["onlyNumbers"])
		elif self.game["complexity"] == 1 and len([1 for i in guess if i in onlyLetters]) != int(self.game["digits"]):
			return render.game(self.game, past, errors["onlyLetters"])
		elif self.game["complexity"] == 2 and len([1 for i in guess if i in numbersLetters]) != int(self.game["digits"]):
			return render.game(self.game, past, errors["numbersLetters"])
		else:
			evaluation = self.password.evaluate(self.game["password"], guess)

			if len(rows) == 0:
				_round = 1
				goldInBag = self.game["goldCoins"] - evaluation["goldCoinsReceived"]
				silverInBag = self.game["silverCoins"] - evaluation["silverCoinsReceived"]
			else:
				_round = len(rows) + 1
				goldInBag = rows[_round - 2][0] - evaluation["goldCoinsReceived"]
				silverInBag = rows[_round - 2][1] - evaluation["silverCoinsReceived"]

			if goldInBag <= 0:
				goldInBag = 0
				evaluation["goldCoinsReceived"] = 0
			if silverInBag <= 0:
				silverInBag = 0
				evaluation["silverCoinsReceived"] = 0

			evaluation["_round"] = _round
			evaluation["goldInBag"] = goldInBag
			evaluation["silverInBag"] = silverInBag
			
			self.writeHistory(evaluation)
			
			#won or lost:
			if ''.join(guess) == self.game["password"] or (goldInBag == 0 and silverInBag == 0):
				self.gameEnded()
				return web.seeother('/gameover')

			return web.seeother('/game')
	
	def gameEnded(self):
		conn = sqlite.connect(appPath + '/data/gamedb.sqlite')
		cur = conn.cursor()
		cur.execute("SELECT * FROM Game WHERE id = ?", (session.game_id,))
		game = rowToDict(cur, cur.fetchone())

		cur.execute("SELECT guess, goldInBag, silverInBag, round FROM History WHERE game_id = ? ORDER BY round DESC", (session.game_id,))
		lastRow = cur.fetchone()
		guess = lastRow[0]
		goldInBag = lastRow[1]
		silverInBag = lastRow[2]
		totalRounds = lastRow[3]
		hasWon = guess == game["password"]

		cur.execute("SELECT goldReceived, silverReceived FROM History WHERE game_id = ?", (session.game_id,))			
		prizeHistory = cur.fetchall()
	
		goldCoinsSpent = 0
		silverCoinsSpent = 0

		for row in prizeHistory:
			goldCoinsSpent += row[0]
			silverCoinsSpent += row[1]

		scoreInstance = code.Score(game["digits"], game["complexity"], goldCoinsSpent, silverCoinsSpent, totalRounds)
		score = scoreInstance.score()

		print score, totalRounds, goldCoinsSpent, silverCoinsSpent, session.game_id
		
		if hasWon:
			won = 1
		else:
			won = 0

		cur.execute("UPDATE Game SET won = ?, score = ?, totalRounds = ?, goldSpent = ?, silverSpent = ? WHERE id = ? ", (won, score, totalRounds, goldCoinsSpent, silverCoinsSpent, session.game_id))
		conn.commit()

		#update Player table:
		cur.execute("SELECT score FROM Game WHERE player_id = ? ", (session.player_id,))
		allScores = cur.fetchall()


		scores = []
		for s in allScores:
			scores.append(s[0])

		totalScore = sum(scores)
		maxScore = max(scores)

		if hasWon:
			cur.execute("UPDATE Player SET wins = wins + 1, games = games + 1, totalScore = ?, maxScore = ? WHERE id = ? ", (totalScore, maxScore, session.player_id) )
		else:
			cur.execute("UPDATE Player SET losses = losses + 1, games = games + 1 WHERE id = ? ", (session.player_id,) )
		conn.commit()
		
		#if maxScore of a player is btw xxx and yyy then badge = diamond vs ruby vs sapphire vs emerald
		if score >= 10000000000:
			badge = 'Diamond'
		elif score >= 1000000:
			badge = 'Emerald'
		elif score >= 100000:
			badge = 'Sapphire'
		else:
			badge = 'Ruby'
		
		print "score", score
		print "badge", badge

		cur.execute('''INSERT INTO Leaderboard(score, badge, player_id) VALUES (?, ?, ?)''', (score, badge, session.player_id) )
		conn.commit()


class GameOver():
	def GET(self):

		if session.player_id == 'guest':
			return web.seeother('/')

		if session.game_id == '0':
			return web.seeother('/setup')

		conn = sqlite.connect(appPath + '/data/gamedb.sqlite')
		cur = conn.cursor()
		cur.execute("SELECT * FROM Game WHERE id = ?", (session.game_id,))
		game = rowToDict(cur, cur.fetchone())

		gameOver = {}

		gameOver["hasWon"] = game["won"] == 1
		gameOver["round"] = game["totalRounds"]

		gameOver["goldInBag"] = game["goldCoins"] - game["goldSpent"] + game["digits"]
		gameOver["silverInBag"] = game["silverCoins"] - game["silverSpent"]

		gameOver["password"] = game["password"]
		gameOver["digits"] = game["digits"]
		gameOver["score"] = game["score"]

		return render.gameover(gameOver)


if __name__ == "__main__":
	app.run()





 



