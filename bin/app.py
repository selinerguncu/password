global conn
global cur
global session
global appPath

import sys
import os
import web
import sqlite3 as sqlite
import locale

appPath = os.getcwd()
print appPath
templatePath = appPath + '/templates'
# to be able to import local modules
sys.path.append(appPath)

from numberGame import code
from numberGame.score import Score
from numberGame.constants import Constants
from utils.errors import errors
from utils.rowToDict import rowToDict
from utils.rowsToDict import rowsToDict
from utils.parseFormData import parseFormData

try:
	locale.setlocale(locale.LC_ALL, 'en_US')
except:
	locale.setlocale(locale.LC_ALL, 'en_US.utf8')

web.config.debug = False
web.config.session_parameters['cookie_name'] = 'session_id'

urls = (
    '/', 'Login',
    '/login', 'Login',
    '/howtoplay', 'HowToPlay',
    '/setup', 'Setup',
    '/game', 'Game',
    '/restart', 'Restart',
    '/quit', 'Quit',
    '/gameover', 'GameOver',
    '/logout', 'Logout'
)

app = web.application(urls, globals())
render = web.template.render(templatePath, base='layout')
db = web.database(dbn='sqlite', db = appPath + '/data/gamedb.sqlite', check_same_thread=False)
store = web.session.DBStore(db, 'sessions')
session = web.session.Session(app, store, initializer={'player_id':'guest', 'game_id': 0})

class HowToPlay():
    def GET(self):
        return render.howtoplay(session.player_id != 'guest')


class Login():
    def __init__(self):
        conn = sqlite.connect(appPath + '/data/gamedb.sqlite')
        cur = conn.cursor()
        cur.execute('''SELECT Leaderboard.score, Leaderboard.badge, Player.username
            FROM Leaderboard JOIN Player ON Leaderboard.player_id = Player.id
            ORDER BY Leaderboard.score DESC LIMIT 5''')
        self.leaders = rowsToDict(cur, cur.fetchall())

        cur.execute('''SELECT totalScore, wins, username FROM Player ORDER BY totalScore DESC LIMIT 5''')
        self.maxLeaders = rowsToDict(cur, cur.fetchall())

        print "maxLeaders", self.maxLeaders
        print self.leaders

    def GET(self):
        if session.player_id == 'guest':
            return render.login(self.leaders, self.maxLeaders)
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
                return render.login(self.leaders, self.maxLeaders, errors["password"])

        else:
            cur.execute('''INSERT INTO Player(username, userpassword) VALUES (?, ?)''', (form_username, form_userPassword))
            conn.commit()
            session.player_id = cur.lastrowid
            return web.seeother('/setup')

class Setup(object):
    def __init__(self):
        levels = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
        digits = [4, 5, 6, 4, 7, 4, 8, 5, 4, 5, 6, 5, 6, 7, 7, 6, 8, 8, 7, 8]
        complexity = [0, 0, 0, 1, 0, 2, 0, 1, 3, 2, 1, 3, 2, 1, 2, 3, 1, 2, 3, 3]
        goldCoins = [20, 30, 37, 40, 42, 45, 47, 53, 55, 59, 64, 71, 73, 76, 93, 94, 96, 122, 125, 198]
        silverCoins = [20, 30, 37, 40, 42, 45, 47, 53, 55, 59, 64, 71, 73, 76, 93, 94, 96, 122, 125, 198]

        self.currentLevel = 0

        self.levelSet = {}
        self.levelSet["levels"] = levels
        self.levelSet["digits"] = digits
        self.levelSet["complexity"] = complexity
        self.levelSet["goldCoins"] = goldCoins
        self.levelSet["silverCoins"] = silverCoins

        #ayni id li adamin butun game lerine bak. en yuksek level i bul. yeni actigin oyuna max level i bir arttir ve ekle
        conn = sqlite.connect(appPath + '/data/gamedb.sqlite')
        cur = conn.cursor()
        cur.execute('''SELECT level, score FROM Game WHERE player_id = ? ORDER BY level DESC''', (session.player_id,))
        lastLevel = cur.fetchone()
        print 'lastLevel', lastLevel

        if lastLevel == None:
            self.currentLevel = 1
        else:
            self.currentLevel = lastLevel[0] + 1

        self.levelSet["currentLevel"] = self.currentLevel


    def GET(self):
        if session.player_id == 'guest':
            return web.seeother('/')

        if session.game_id == 0:
            return render.setup(self.levelSet)
        else:
            conn = sqlite.connect(appPath + '/data/gamedb.sqlite')
            cur = conn.cursor()
            cur.execute('''SELECT won FROM Game WHERE id = ?''', (session.game_id,))
            gameRow = cur.fetchone()

            if gameRow[0] in [0, 1]:
                return render.setup(self.levelSet)
            else:
                return web.seeother('/game')

    def POST(self):
        data = parseFormData(web.data())
        print data
        conn = sqlite.connect(appPath + '/data/gamedb.sqlite')
        cur = conn.cursor()

        error = self.validate(data)
        warning = None

        if error == None:
            warning = self.hasWarning(data)

        if (error == None and warning == None) or (error == None and int(data["force"]) == 1):
            cur.execute('''
                INSERT INTO Game(digits, complexity, goldCoins, silverCoins, level, player_id)
                VALUES (?, ?, ?, ?, ?, ?)
                ''', (data["digits"], data["complexity"], data["goldCoins"], data["silverCoins"], self.currentLevel, session.player_id))
            conn.commit()
            session.game_id = cur.lastrowid
            return web.seeother('/game')

        elif error != None:
            return render.setup(self.levelSet, errors[error], data, True)
        elif error == None and warning != None:
            return render.setup(self.levelSet, errors[warning], data)

    def hasWarning(self, data):
        warning = None
        goldCoins = int(data["goldCoins"])
        silverCoins = int(data["silverCoins"])
        complexity = int(data["complexity"])
        digits = int(data["digits"])

        print goldCoins, silverCoins, complexity, digits

        if goldCoins > 120 or silverCoins > 120:
            warning = "max100"
        elif (goldCoins < 10 and goldCoins > 0) or (silverCoins < 10 and silverCoins > 0):
            warning = "min20"
        else:
            if goldCoins < 50 and complexity == 1:
                warning = "gold50complex"
            elif goldCoins < 70 and complexity == 2:
                warning = "gold70complex"
            elif goldCoins < 100 and complexity == 3:
                warning = "gold100complex"
            if goldCoins < 30 and digits == 4:
                warning = "gold30"
            elif goldCoins < 30 and digits == 5:
                warning = "gold30"
            elif goldCoins < 40 and digits == 6:
                warning = "gold40"
            elif goldCoins < 50 and digits == 7:
                warning = "gold50"
            elif goldCoins < 60 and digits == 8:
                warning = "gold60"
            elif silverCoins < 50 and complexity == 1:
                warning = "silver50complex"
            elif silverCoins < 70 and complexity == 2:
                warning = "silver70complex"
            elif silverCoins < 100 and complexity == 3:
                warning = "silver100complex"
            elif silverCoins < 30 and digits == 4:
                warning = "silver30"
            elif silverCoins < 30 and digits == 5:
                warning = "silver30"
            elif silverCoins < 40 and digits == 6:
                warning = "silver40"
            elif silverCoins < 50 and digits == 7:
                warning = "silver50"
            elif silverCoins < 60 and digits == 8:
                warning = "silver60"
        return warning

    def validate(self, data):
        err = None
        goldCoins = data["goldCoins"]
        silverCoins = data["silverCoins"]

        if goldCoins == "" and silverCoins != "" or goldCoins == '0' and silverCoins != '0':
            err = "goldAmount"
        elif silverCoins == "" and goldCoins != "" or silverCoins == '0' and goldCoins != '0':
            err = "silverAmount"
        elif silverCoins == "" and goldCoins == "" or silverCoins == '0' and goldCoins == '0':
            err = "goldSilverAmount"
        print silverCoins, goldCoins, err, silverCoins == "", goldCoins == "", silverCoins == 0, goldCoins == 0
        return err

class Restart():
    def __init__(self):
        conn = sqlite.connect(appPath + '/data/gamedb.sqlite')
        cur = conn.cursor()
        cur.execute('''SELECT * FROM Game WHERE id = ?''', (session.game_id,))
        gameRow = cur.fetchone()

        if gameRow == None:
            return web.seeother("/game")

        self.game = rowToDict(cur, gameRow)

    def lose(self):
        conn = sqlite.connect(appPath + '/data/gamedb.sqlite')
        cur = conn.cursor()

        cur.execute("UPDATE Game SET won = ? WHERE id = ? ", (0, session.game_id))
        conn.commit()

    def createNewGame(self):
        conn = sqlite.connect(appPath + '/data/gamedb.sqlite')
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO Game(digits, complexity, goldCoins, silverCoins, level, player_id)
            VALUES (?, ?, ?, ?, ?, ?)
            ''', (self.game["digits"], self.game["complexity"], self.game["goldCoins"], self.game["silverCoins"], self.game["level"], session.player_id))
        conn.commit()
        # update session
        session.game_id = cur.lastrowid

    def GET(self):
        conn = sqlite.connect(appPath + '/data/gamedb.sqlite')
        cur = conn.cursor()

        self.lose()
        self.createNewGame()

        return web.seeother("/game")


class Quit(Restart):

    def GET(self):
        conn = sqlite.connect(appPath + '/data/gamedb.sqlite')
        cur = conn.cursor()

        self.lose()

        return web.seeother("/setup")



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

        cur.execute('''SELECT round, guess, goldReceived, silverReceived, goldInBag, silverInBag FROM History WHERE game_id = ? ORDER BY round DESC''', (session.game_id,))
        history = cur.fetchall()

        past = []
        for row in history:
            past.append(row)

        print 'self.game["complexity"]', self.game['complexity']

        return render.game(self.game, past)


    def POST(self):
        print self.game["password"]
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

        onlyNumbers = Constants["onlyNumbers"]
        onlyLetters = Constants["onlyLetters"]
        numbersLowercaseLetters = Constants["numbersLowercaseLetters"]
        uppercaseLetters = Constants["uppercaseLetters"]
        numbersAllLetters = Constants["numbersAllLetters"]

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
        elif self.game["complexity"] == 3 and len(guess) > len(set(guess)):
            return render.game(self.game, past, errors["uniqueNumbersAllLetters"])
        elif self.game["complexity"] == 0 and len([1 for i in guess if i in onlyNumbers]) != int(self.game["digits"]):
            return render.game(self.game, past, errors["onlyNumbers"])
        elif self.game["complexity"] == 1 and len([1 for i in guess if i in onlyLetters]) != int(self.game["digits"]):
            return render.game(self.game, past, errors["onlyLetters"])
        elif self.game["complexity"] == 2 and len([1 for i in guess if i in numbersLowercaseLetters]) != int(self.game["digits"]):
            return render.game(self.game, past, errors["numbersLetters"])
        elif self.game["complexity"] == 3 and len([1 for i in guess if i in numbersAllLetters]) != int(self.game["digits"]):
            return render.game(self.game, past, errors["numbersAllLetters"])
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

        scoreVariables = {
            "digits" : game["digits"],
            "complexity" : game["complexity"],
            "goldCoins" : game["goldCoins"],
            "silverCoins" : game["silverCoins"],
            "totalRounds" : game["totalRounds"],
            "goldSpent" : game["goldSpent"],
            "silverSpent" : game["silverSpent"]
        }

        scoreInstance = Score(scoreVariables)
        score = scoreInstance.calculateScore()

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

        cur.execute('''INSERT INTO Leaderboard(score, badge, player_id, game_id) VALUES (?, ?, ?, ?)''', (score, badge, session.player_id, session.game_id) )
        conn.commit()


class GameOver():
    def __init__(self):
        conn = sqlite.connect(appPath + '/data/gamedb.sqlite')
        cur = conn.cursor()
        cur.execute('''SELECT Leaderboard.score, Leaderboard.badge, Player.username,  Leaderboard.game_id
            FROM Leaderboard JOIN Player ON Leaderboard.player_id = Player.id
            ORDER BY Leaderboard.score DESC LIMIT 5''')
        leaderRows = cur.fetchall()
        self.leaders = rowsToDict(cur, leaderRows)


    def GET(self):

        if session.player_id == 'guest':
            return web.seeother('/')

        if session.game_id == '0':
            return web.seeother('/setup')

        conn = sqlite.connect(appPath + '/data/gamedb.sqlite')
        cur = conn.cursor()
        cur.execute("SELECT * FROM Game WHERE id = ?", (session.game_id,))
        game = rowToDict(cur, cur.fetchone())

        cur.execute('''SELECT Leaderboard.score, Leaderboard.badge, Player.username, Leaderboard.game_id
            FROM Leaderboard JOIN Player ON Leaderboard.player_id = Player.id
            WHERE Leaderboard.score = ? AND Player.id = ?''', (game["score"], session.player_id))
        gameInLeaderboard = rowToDict(cur, cur.fetchone())

        if gameInLeaderboard in self.leaders:
            gameInLeaderboard['inHighScores'] = True
        else:
            gameInLeaderboard['inHighScores'] = False

        gameOver = {}

        gameOver["hasWon"] = game["won"] == 1
        gameOver["round"] = game["totalRounds"]

        gameOver["goldInBag"] = game["goldCoins"] - game["goldSpent"] + game["digits"]
        gameOver["silverInBag"] = game["silverCoins"] - game["silverSpent"]

        gameOver["password"] = game["password"]
        gameOver["digits"] = game["digits"]

        gameOver["score"] = locale.format("%d", game["score"], grouping=True)

        return render.gameover(gameOver, self.leaders, session.game_id, gameInLeaderboard)

class Logout():
    def GET(self):
        session.kill()
        return web.seeother('/')

if __name__ == "__main__":
    app.run()









