import sqlite3

import web
import app

global appPath
appPath = "/Users/selinerguncu/Desktop/PythonProjects/Fun Projects/TestGame"

conn = sqlite3.connect(appPath + '/data/gamedb.sqlite')
cur = conn.cursor()

cur.executescript('''
	
DROP TABLE IF EXISTS Leaderboard;
DROP TABLE IF EXISTS Player;
DROP TABLE IF EXISTS Game;
DROP TABLE IF EXISTS sessions;

CREATE TABLE Leaderboard (
	id	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	username	TEXT,
	score	INTEGER,
	badge	TEXT DEFAULT NONE,
	player_id  INTEGER,
	FOREIGN KEY(player_id) REFERENCES Player(id)
);

CREATE TABLE Player (
	id	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	username	TEXT UNIQUE,
	userpassword	TEXT,
	games	INTEGER DEFAULT 0,
	wins	INTEGER DEFAULT 0,
	losses   INTEGER DEFAULT 0,
	maxScore 	INTEGER DEFAULT 0,
	totalScore INTEGER DEFAULT 0
);

CREATE TABLE Game (
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	username	TEXT,
	gameover	TEXT,
	score	INTEGER DEFAULT 0,
	totalRounds	INTEGER,
	digits	INTEGER,
	complexity	INTEGER,
	goldSpent	INTEGER,
	silverSpent	INTEGER,
	player_id	INTEGER,
	FOREIGN KEY(player_id) REFERENCES Player(id)
);

CREATE TABLE sessions (
    session_id char(128) UNIQUE NOT NULL,
    atime timestamp NOT NULL default current_timestamp,
    data TEXT
)

''')

# cur.execute (
# 	''' INSERT INTO sessions (username) VALUES (?) ''' , (app.session.get('username'), )
# 	)

conn.commit()

conn.close()









