global conn
global cur
global session
global appPath

import sys
import os
import web
import sqlite3 as sqlite
import locale
import logging
logging.getLogger("requests").setLevel(logging.ERROR)

appPath = os.getcwd()
templatePath = appPath + '/templates'
# to be able to import local modules
sys.path.append(appPath)
reload(sys)
sys.setdefaultencoding('utf-8')

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
    '/leaderboard', "Leaderboard",
    '/login', 'Login',
    '/profile', 'Profile',
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
        howToPlayLevels = Constants["howToPlayLevels"]
        howToPlayRecommended = Constants["howToPlayRecommended"]

        return render.howtoplay(session.player_id != 'guest', howToPlayLevels, howToPlayRecommended)


class Login():
    def __init__(self):
        conn = sqlite.connect(appPath + '/data/gamedb.sqlite')
        cur = conn.cursor()
        cur.execute('''SELECT Leaderboard.score, Leaderboard.badge, Player.username
            FROM Leaderboard JOIN Player ON Leaderboard.player_id = Player.id
            ORDER BY Leaderboard.score DESC LIMIT 5''')
        self.leaders = rowsToDict(cur, cur.fetchall())

        for k in range(len(self.leaders)):
            self.leaders[k]["score"] = locale.format("%d", self.leaders[k]["score"], grouping=True)

        cur.execute('''SELECT totalScore, wins, username FROM Player WHERE totalScore > 0
            ORDER BY totalScore DESC LIMIT 5''')
        self.maxLeaders = rowsToDict(cur, cur.fetchall())

        for i in range(len(self.maxLeaders)):
            self.maxLeaders[i]["totalScore"] = locale.format("%d", self.maxLeaders[i]["totalScore"], grouping=True)

    def getPage(self):
        params = web.input()
        if "register" in params.keys():
            return 'register'
        if "forgot" in params.keys():
            return 'forgot'
        if session.player_id == 'guest':
            return 'login'

    def getError(self):
        params = web.input()
        if "error" in params.keys():
            return errors[params["error"]]
        else:
            return None

    def GET(self):
        params = web.input()
        page = self.getPage()
        error = self.getError()

        # if page in [ 'register', 'forgot' ]:
        if page in [ 'register' ]:
            return render.login(self.leaders, self.maxLeaders, page = page, error = error)
        if session.player_id == 'guest':
            return render.login(self.leaders, self.maxLeaders, error = error)
        else:
            return web.seeother('/setup')


    def POST(self):
        data = parseFormData(web.data())

        if 'registerForm' in data.keys():
            self.register(data)
        elif 'forgotForm' in data.keys():
            self.forgotPassword(data)
        elif 'loginForm' in data.keys():
            self.login(data)
        else:
            return web.seeother('/login?error=allBlank')


    def login(self, data):

        data = parseFormData(web.data())
        conn = sqlite.connect(appPath + '/data/gamedb.sqlite')
        cur = conn.cursor()

        if not "username" in data.keys() and not "userpassword" in data.keys():
            return web.seeother('/login?error=allBlank')

        if not "username" in data.keys():
            return web.seeother('/login?error=usernameBlank')
        form_username = data["username"]

        if not "userpassword" in data.keys():
            return web.seeother('/login?error=passwordBlank')
        form_userPassword = data["userpassword"]

        cur.execute('''SELECT userpassword, id FROM Player WHERE username = ?''', (form_username,))
        pass_and_id = cur.fetchone()

        # if pass_and_id != None:
        db_userPassword = pass_and_id[0]
        player_id = pass_and_id[1]

        if db_userPassword == form_userPassword:
            session.player_id = player_id
            return web.seeother('/setup')
        else:
            return web.seeother('/login?error=password')


    def register(self, data):

        conn = sqlite.connect(appPath + '/data/gamedb.sqlite')
        cur = conn.cursor()

        try:
            # form_secretQuestion = data["secretQuestion"]
            # form_secretAnswer = data["secretAnswer"]
            form_secretQuestion = None
            form_secretAnswer = None
            form_registerUsername = data["registerUsername"]
            form_registerUserpassword = data["registerUserpassword"]
            form_registerConfirmpassword = data["registerConfirmpassword"]
        except:
            return web.seeother('/login?error=allBlank&register')

        if form_registerConfirmpassword != form_registerUserpassword:
            return web.seeother('/login?error=confirmPassword&register')

        cur.execute('''SELECT id FROM Player WHERE username = ?''', (form_registerUsername,))
        idRow = cur.fetchone()
        if idRow:
            return web.seeother('/login?error=existingUser&register')

        cur.execute('''INSERT INTO Player(username, userpassword, secretQuestion, secretAnswer)
            VALUES (?, ?, ?, ?)''', (form_registerUsername, form_registerUserpassword, form_secretQuestion, form_secretAnswer))
        conn.commit()
        session.player_id = cur.lastrowid
        return web.seeother('/setup')


    # def forgotPassword(self, data):

    #     conn = sqlite.connect(appPath + '/data/gamedb.sqlite')
    #     cur = conn.cursor()

    #     try:
    #         form_secretQuestion = data["secretQuestion"]
    #         form_secretAnswer = data["secretAnswer"]
    #         form_username = data["username"]
    #     except:
    #         return web.seeother('/login?error=allBlank&forgot')

    #     cur.execute('''SELECT secretQuestion, secretAnswer FROM Player WHERE username = ?''', (form_username,))
    #     secretKeys = cur.fetchone()

    #     secretQuestion = secretKeys[0]
    #     secretAnswer = secretKeys[1]

    #     if secretQuestion is form_secretQuestion and secretAnswer is form_secretAnswer:
    #         return

    #     # return "yarim"
    #     # return render.login(self.leaders, self.maxLeaders, error = errors["secretQuestion"], forgot = True, secretQuestion = secretQuestion)
    #     # secret question yapmak daha mantikli


class Profile():

    def GET(self):
        conn = sqlite.connect(appPath + '/data/gamedb.sqlite')
        cur = conn.cursor()
        cur.execute('''SELECT * FROM Player WHERE id = ?''', (session.player_id,))
        playerRow = cur.fetchone()
        player = rowToDict(cur, playerRow)

        cur.execute('''SELECT Game.*, Leaderboard.badge
            FROM Game JOIN Leaderboard ON Leaderboard.game_id = Game.id
            WHERE Game.player_id = ? ORDER BY level DESC''', (session.player_id,))
        allGamesWithBadges = rowsToDict(cur, cur.fetchall())

        cur.execute('''SELECT * FROM Game
            WHERE player_id = ? ORDER BY level DESC''', (session.player_id,))
        allGames = rowsToDict(cur, cur.fetchall())

        for game in allGames:
            game["badge"] = '-'
            for gameWithBadge in allGamesWithBadges:
                if gameWithBadge['id'] == game['id']:
                    game["badge"] = gameWithBadge["badge"]

        cur.execute('''SELECT History.game_id, History.goldReceived, History.silverReceived, History.round
            FROM History JOIN Game JOIN Player ON History.game_id = Game.id AND Game.player_id = Player.id
            WHERE Player.id = ? ORDER BY level DESC''', (session.player_id,))

        historyRows = cur.fetchall()
        allHistory = rowsToDict(cur, historyRows)

        allGamesHistory = {}
        for game in allGames:
            gameId = game["id"]
            allGamesHistory[gameId] = {}
            allGamesHistory[gameId]["round"] = 0
            allGamesHistory[gameId]["goldReceived"] = 0
            allGamesHistory[gameId]["silverReceived"] = 0
            for history in allHistory:
                if history["game_id"] == gameId:
                    allGamesHistory[gameId]["goldReceived"] += history["goldReceived"]
                    allGamesHistory[gameId]["silverReceived"] += history["silverReceived"]
                    if history["round"] > allGamesHistory[gameId]["round"]:
                        allGamesHistory[gameId]["round"] = history["round"]

        for game in allGames:
            game["goldSpent"] = allGamesHistory[game["id"]]["goldReceived"]
            game["silverSpent"] = allGamesHistory[game["id"]]["silverReceived"]
            game["totalRounds"] = allGamesHistory[game["id"]]["round"]

        player["maxScore"] = locale.format("%d", player["maxScore"], grouping=True)
        player["totalScore"] = locale.format("%d", player["totalScore"], grouping=True)

        for i in range(len(allGames)):
            allGames[i]["score"] = locale.format("%d", allGames[i]["score"], grouping=True)

        return render.profile(player, allGames)


class Leaderboard():

    def GET(self):
        conn = sqlite.connect(appPath + '/data/gamedb.sqlite')
        cur = conn.cursor()
        isLoggedIn = session.player_id != 'guest'
        # tab=game&gamePage=5&playerPage=3
        params = web.input()
        tab = 'game'
        gamePage = 1
        playerPage = 1
        limit = 20

        if "tab" in params.keys():
            tab = params.tab
        if "gamePage" in params.keys():
            gamePage = int(params.gamePage)
        if "playerPage" in params.keys():
            playerPage = int(params.playerPage)

        gameSkip = (gamePage-1) * limit
        playerSkip = (playerPage-1) * limit

        cur.execute('''SELECT COUNT(*) FROM Leaderboard''')
        gameCount = cur.fetchone()[0]
        gamePages = (gameCount / limit) + 1

        cur.execute('''SELECT COUNT(*) FROM Player WHERE totalScore > 0''')
        playerCount = cur.fetchone()[0]
        playerPages = (playerCount / limit) + 1

        cur.execute('''SELECT Leaderboard.score, Leaderboard.badge, Player.username
            FROM Leaderboard JOIN Player ON Leaderboard.player_id = Player.id
            WHERE Leaderboard.score > 0 ORDER BY Leaderboard.score DESC LIMIT ? OFFSET ?''', (limit, gameSkip))

        games = rowsToDict(cur, cur.fetchall())
        for k in range(len(games)):
            games[k]["score"] = locale.format("%d", games[k]["score"], grouping=True)

        cur.execute('''SELECT totalScore, wins, username FROM Player WHERE totalScore > 0
            ORDER BY totalScore DESC LIMIT ? OFFSET ?''', (limit, playerSkip))
        players = rowsToDict(cur, cur.fetchall())

        for i in range(len(players)):
            players[i]["totalScore"] = locale.format("%d", players[i]["totalScore"], grouping=True)

        return render.leaderboard(games, players, gamePage, playerPage, gamePages, playerPages, tab, isLoggedIn)


class Setup(object):
    def __init__(self):
        levels = Constants["levels"]
        digits = Constants["digits"]
        complexity = Constants["complexity"]
        goldCoins = Constants["goldCoins"]
        silverCoins = Constants["silverCoins"]

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
        cur.execute('''SELECT level, score, won FROM Game WHERE player_id = ? AND won = 1 ORDER BY level DESC''', (session.player_id,))
        last = cur.fetchone()

        print last

        if last == None:
            self.currentLevel = 1
        else:
            lastLevel = rowToDict(cur, last)
            if lastLevel["won"] == 1 and lastLevel["level"] != 0:
                self.currentLevel = lastLevel["level"] + 1
            elif lastLevel["level"] == 0:
                self.currentLevel = 1
            elif lastLevel["won"] == 0:
                self.currentLevel = lastLevel["level"]

        cur.execute('''SELECT username FROM Player WHERE id = ?''', (session.player_id,))
        self.player = rowToDict(cur, cur.fetchone())

        self.levelSet["currentLevel"] = self.currentLevel

    def GET(self):
        conn = sqlite.connect(appPath + '/data/gamedb.sqlite')
        cur = conn.cursor()
        if session.player_id == 'guest':
            return web.seeother('/')

        cur.execute('''SELECT won, id, level FROM Game WHERE player_id = ? AND won IS NULL''', (session.player_id,))
        unfinishedGames = rowsToDict(cur, cur.fetchall())
        return render.setup(self.player, self.levelSet, None, None, False, unfinishedGames)

    def POST(self):
        data = parseFormData(web.data())

        if "gameid" in data.keys():
          session.game_id = data["gameid"]
          return web.seeother('/game')

        conn = sqlite.connect(appPath + '/data/gamedb.sqlite')
        cur = conn.cursor()

        error = self.validate(data)
        warning = None

        if error == None:
            warning = self.hasWarning(data)

        if (error == None and warning == None) or (error == None and int(data["force"]) == 1):
            if "level" not in data.keys():
                data["level"] = "0"
            cur.execute('''
                INSERT INTO Game(digits, complexity, goldCoins, silverCoins, level, player_id)
                VALUES (?, ?, ?, ?, ?, ?)
                ''', (data["digits"], data["complexity"], data["goldCoins"], data["silverCoins"], data["level"], session.player_id))
            conn.commit()
            session.game_id = cur.lastrowid
            return web.seeother('/game')

        elif error != None:
            return render.setup(self.player, self.levelSet, errors[error], data, True)
        elif error == None and warning != None:
            return render.setup(self.player, self.levelSet, errors[warning], data)

    def hasWarning(self, data):
        warning = None
        goldCoins = int(data["goldCoins"])
        silverCoins = int(data["silverCoins"])
        complexity = int(data["complexity"])
        digits = int(data["digits"])

        if 501 > goldCoins >= 5 and 501 > silverCoins >= 5:
            if goldCoins < 56 and complexity == 1:
                warning = "gold56complex"
            elif goldCoins < 82 and complexity == 2:
                warning = "gold82complex"
            elif goldCoins < 136 and complexity == 3:
                warning = "gold136complex"
            if goldCoins < 20 and digits == 4:
                warning = "gold20"
            elif goldCoins < 30 and digits == 5:
                warning = "gold30"
            elif goldCoins < 37 and digits == 6:
                warning = "gold37"
            elif goldCoins < 42 and digits == 7:
                warning = "gold42"
            elif goldCoins < 46 and digits == 8:
                warning = "gold46"
            elif silverCoins < 56 and complexity == 1:
                warning = "silver56complex"
            elif silverCoins < 82 and complexity == 2:
                warning = "silver82complex"
            elif silverCoins < 136 and complexity == 3:
                warning = "silver136complex"
            elif silverCoins < 20 and digits == 4:
                warning = "silver20"
            elif silverCoins < 30 and digits == 5:
                warning = "silver30"
            elif silverCoins < 37 and digits == 6:
                warning = "silver37"
            elif silverCoins < 42 and digits == 7:
                warning = "silver42"
            elif silverCoins < 46 and digits == 8:
                warning = "silver46"
        return warning

    def validate(self, data):
        err = None
        try:
            goldCoins = int(data["goldCoins"])
        except:
            goldCoins = ""
            data["goldCoins"] = None
        try:
            silverCoins = int(data["silverCoins"])
        except:
            silverCoins = ""
            data["goldCoins"] = None
            #burayi okumuyor!!!!
        if int(data["digits"]) > 10 and int(data["complexity"]) == 1:
            err = "outOfRange"

        if (goldCoins != "" and silverCoins != "") and (goldCoins > 500 or silverCoins > 500):
            err = "max500"
        elif (goldCoins == "" and silverCoins != "") or (goldCoins < 5 and silverCoins >= 5):
            err = "goldAmount"
        elif (silverCoins == "" and goldCoins != "") or (silverCoins < 5 and goldCoins >= 5):
            err = "silverAmount"
        elif (silverCoins == "" and goldCoins == "") or (silverCoins < 5 and goldCoins < 5):
            err = "goldSilverAmount"
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
        session.game_id = 0

        return web.seeother("/setup")


class Game(object):
    def __init__(self):
        self.count = 0
        self.game = None
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

        if not self.game:
            return web.seeother('/setup')

        conn = sqlite.connect(appPath + '/data/gamedb.sqlite')
        cur = conn.cursor()

        cur.execute('''SELECT round, guess, goldReceived, silverReceived, goldInBag, silverInBag FROM History WHERE game_id = ? ORDER BY round DESC''', (session.game_id,))
        history = cur.fetchall()

        past = []
        for row in history:
            past.append(row)

        return render.game(self.game, past)


    def POST(self):
        print self.game["password"]
        data = parseFormData(web.data())
        guess = []

        # if data["win"]:
        #     for i in self.game["password"]:
        #         guess.append(i)
        # else:
        try:
            guess.append(data["first"])
            guess.append(data["second"])
            guess.append(data["third"])
            guess.append(data["fourth"])
            guess.append(data["fifth"])
            guess.append(data["sixth"])
            guess.append(data["seventh"])
            guess.append(data["eighth"])
            guess.append(data["ninth"])
            guess.append(data["tenth"])
            guess.append(data["eleventh"])
            guess.append(data["twelfth"])
            guess.append(data["thirteenth"])
            guess.append(data["fourteenth"])
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
        cur.execute("SELECT round, guess, goldReceived, silverReceived, goldInBag, silverInBag FROM History WHERE game_id = ? ORDER BY round DESC", (session.game_id,))
        rows = cur.fetchall()

        past = []
        for row in rows:
            past.append((row[0], row[1], row[2], row[3], row[4], row[5]))

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
                goldInBag = rows[0][4] - evaluation["goldCoinsReceived"]
                silverInBag = rows[0][5] - evaluation["silverCoinsReceived"]

            evaluation["_round"] = _round
            evaluation["goldInBag"] = goldInBag
            evaluation["silverInBag"] = silverInBag

            self.writeHistory(evaluation)

            #won or lost:
            if ''.join(guess) == self.game["password"] or (goldInBag <= 0 and silverInBag <= 0):
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
        badge = None
        hasWon = guess == game["password"]

        cur.execute("SELECT goldReceived, silverReceived FROM History WHERE game_id = ?", (session.game_id,))
        prizeHistory = cur.fetchall()

        goldCoinsSpent = 0
        silverCoinsSpent = 0

        for row in prizeHistory:
            goldCoinsSpent += row[0]
            silverCoinsSpent += row[1]


        if hasWon:
            won = 1
            goldCoinsSpent -= game["digits"]
            scoreVariables = {
                "digits" : game["digits"],
                "complexity" : game["complexity"],
                "goldCoins" : game["goldCoins"],
                "silverCoins" : game["silverCoins"],
                "totalRounds" : totalRounds,
                "goldSpent" : goldCoinsSpent,
                "silverSpent" : silverCoinsSpent
            }
            scoreInstance = Score(scoreVariables)
            score = scoreInstance.calculateScore()

        else:
            won = 0
            score = 0

        if hasWon:
            highScoresByLevel = scoreInstance.getMaxScores()
            print highScoresByLevel

            print "RAW SCORE", score

            scoreElements = []
            baseScore = [0, 2000, 10000, 20000, 50000, 80000, 110000, 140000, 170000, 200000, 230000, 250000, 290000, 360000, 430000, 500000, 550000, 650000, 750000, 850000]
            jumpBtwLevels = [2000, 8000, 10000, 30000, 30000, 30000, 30000, 30000, 30000, 30000, 20000, 40000, 70000, 70000, 70000, 50000, 100000, 100000, 100000, 150000]
            badgeForLevels = ["-", "-", "-", "Ruby", "Ruby",
            "Sapphire", "Sapphire", "Sapphire", "Sapphire", "Sapphire",
            "Emerald", "Emerald", "Emerald", "Emerald", "Emerald",
            "Diamond", "Diamond", "Diamond", "Diamond", "Diamond"]

            for i in range(len(highScoresByLevel)):
                if i < 1:
                    minScore = 0
                else:
                    minScore = highScoresByLevel[i-1]

                badge = badgeForLevels[i]
                base = baseScore[i]
                jump = jumpBtwLevels[i]
                maxScore = highScoresByLevel[i]
                scoreElements.append((i+1, badge, base, minScore, maxScore, jump))

            for i in scoreElements:
                scoreLevel = i[0]
                baseScore = i[2]
                minScore = i[3]
                maxScore = i[4]
                jump = i[5]
                if minScore < score <= maxScore:
                    score = baseScore + ((score - baseScore) * jump / (maxScore - baseScore))
                    badge = i[1]

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

        print 'gameEnded'
        print score
        print 'gameEnded'

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

        for i in range(len(self.leaders)):
            self.leaders[i]["score"] = locale.format("%d", self.leaders[i]["score"], grouping=True)

        cur.execute('''SELECT totalScore, wins, username, id FROM Player WHERE wins > 0 ORDER BY totalScore DESC LIMIT 5''')
        maxLeaderRows = cur.fetchall()
        self.maxLeaders = rowsToDict(cur, maxLeaderRows)

        for i in range(len(self.maxLeaders)):
            self.maxLeaders[i]["totalScore"] = locale.format("%d", self.maxLeaders[i]["totalScore"], grouping=True)


    def GET(self):

        if session.player_id == 'guest':
            return web.seeother('/')

        if session.game_id == '0':
            return web.seeother('/setup')

        conn = sqlite.connect(appPath + '/data/gamedb.sqlite')
        cur = conn.cursor()
        cur.execute("SELECT * FROM Game WHERE id = ?", (session.game_id,))
        game = rowToDict(cur, cur.fetchone())

        cur.execute("SELECT * FROM Player WHERE id = ?", (session.player_id,))
        player = rowToDict(cur, cur.fetchone())

        cur.execute('''SELECT Leaderboard.score, Leaderboard.badge, Player.username, Leaderboard.game_id
            FROM Leaderboard JOIN Player ON Leaderboard.player_id = Player.id
            WHERE Leaderboard.score = ? AND Player.id = ?''', (game["score"], session.player_id))
        aa = cur.fetchone()
        gameInLeaderboard = rowToDict(cur, aa)

        gameInLeaderboard["score"] = locale.format("%d", game["score"], grouping=True)

        if gameInLeaderboard in self.leaders:
            gameInLeaderboard['inHighScores'] = True
        else:
            gameInLeaderboard['inHighScores'] = False

        cur.execute('''SELECT totalScore, wins, username, id FROM Player WHERE id = ?
            ORDER BY totalScore DESC LIMIT 5''', (session.player_id,))
        inMaxLeaders = cur.fetchone()
        gameInMaxLeaders = rowToDict(cur, inMaxLeaders)

        gameInMaxLeaders["totalScore"] = locale.format("%d", player["totalScore"], grouping=True)

        if gameInMaxLeaders in self.maxLeaders:
            gameInMaxLeaders['inMaxScores'] = True
        else:
            gameInMaxLeaders['inMaxScores'] = False

        gameOver = {}

        gameOver["hasWon"] = game["won"] == 1
        gameOver["round"] = game["totalRounds"]
        gameOver["goldInBag"] = game["goldCoins"] - game["goldSpent"]
        gameOver["silverInBag"] = game["silverCoins"] - game["silverSpent"]
        gameOver["password"] = game["password"]
        gameOver["digits"] = game["digits"]
        gameOver["level"] = game["level"]

        gameOver["score"] = locale.format("%d", game["score"], grouping=True)

        return render.gameover(gameOver, self.leaders, self.maxLeaders, session.game_id, session.player_id, gameInLeaderboard, gameInMaxLeaders)


class Logout():
    def GET(self):
        session.kill()
        return web.seeother('/')

if __name__ == "__main__":
    app.run()
