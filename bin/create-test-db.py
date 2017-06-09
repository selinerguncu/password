global conn
global cur
global appPath

import sys
import os
import sqlite3 as sqlite
import random
import web

appPath = os.getcwd()

# to be able to import local modules
sys.path.append(appPath)

db = web.database(dbn='sqlite', db = appPath + '/data/gamedb.sqlite', check_same_thread=False)

conn = sqlite.connect(appPath + '/data/gamedb.sqlite')
cur = conn.cursor()


for i in range(115):
    username = i
    userpassword = '123123'
    games = 300
    wins = 190
    losses = 110
    maxScore = 0
    totalScore = random.randrange(10000, 100000000)
    cur.execute('''
        INSERT INTO Player(username, userpassword, games, wins, losses, maxScore, totalScore)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (username, userpassword, games, wins, losses, maxScore, totalScore))
    conn.commit()

for i in range(300):
    password = random.randrange(100, 1000000)
    level = 1
    won = 1
    score = random.randrange(100, 1000000)
    totalRounds = random.randrange(1, 100)
    digits = 1
    complexity = 1
    goldCoins = 20
    silverCoins = 20
    goldSpent = 10
    silverSpent = 10
    player_id = random.randrange(1, 115, 1)
    cur.execute('''
        INSERT INTO Game(password, level, won, score, totalRounds, digits, complexity, goldCoins, silverCoins, goldSpent, silverSpent, player_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (password, level, won, score, totalRounds, digits, complexity, goldCoins, silverCoins, goldSpent, silverSpent, player_id))
    conn.commit()

for i in range(300):
    score = random.randrange(100, 1000000)
    badge = 'Ruby'
    player_id = random.randrange(1, 115, 1)
    game_id = random.randrange(1, 300, 1)
    cur.execute('''
        INSERT INTO Leaderboard(score, badge, player_id, game_id)
        VALUES (?, ?, ?, ?)
        ''', (score, badge, player_id, game_id))
    conn.commit()
