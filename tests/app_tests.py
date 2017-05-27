from nose.tools import *

from bin.app import app	
from numberGame import code

from tests.tools import assert_response 
from utils.parseFormData import parseFormData
from utils.getSession import getSession
import time

# def test_root():
# 	#should get a 404 on the / URL
# 	resp = app.request("/")
# 	assert_response(resp, status="404")

# def test_login():
# 	#test the first GET request to /login
# 	resp = app.request("/login")
# 	assert_response(resp)

# def test_username():
# 	data = {'username': '', 'password':'xxx'}
# 	resp = app.request("/login", method="POST", data=data)
# 	assert_response(resp, contains="Please insert a valid username.")

def test_parseFormData():
	rawData = "username=xxx&password=1q2w3e4r"
	assert_equal(parseFormData(rawData)["username"], "xxx")
	assert_equal(parseFormData(rawData)["password"], "1q2w3e4r")

def test_sessionUsername():
	data = {'username': 'xxx', 'password':'1q2w3e4r'}
	resp = app.request("/login", method="POST", data=data)
	# time.sleep(5)
	session = getSession(app)
	print 'test', session
# 	print 'test', session.get("username")
# 	# print resp
# 	assert_equal(session.get("username"), "xxx")

# # def test_sessionPassword():
# # 	data = {'username': 'xxx', 'password':'1q2w3e4r'}
# # 	resp = app.request("/login", method="POST", data=data)
# # 	assert_response(resp.session.password, matches="1q2w3e4r")

# # def test_password():
# # 	data = {'username': 'xxx', 'password':''}
# # 	resp = app.request("/login", method="POST", data=data)
# # 	assert_response(resp, contains="Please create a valid password.")

def test_intro():
	#test the first GET request to /intro
	resp = app.request("/intro")
	assert_response(resp)

def test_howtoplay():
	#test the first GET request to /howtoplay
	resp = app.request("/howtoplay")
	assert_response(resp)

def test_sample2():
	#test the first GET request to /sample2
	resp = app.request("/sample2")
	assert_response(resp)

def test_setup():
	#test the first GET request to /setup
	resp = app.request("/setup")
	assert_response(resp)

def test_setupErrors():
	data1 = {'digits': '4', 'complexity':'0', 'goldCoins': '', 'silverCoins': '30'}
	resp = app.request("/setup", method="POST", data=data1)
	assert_response(resp, contains="You have to have some amount of Gold coins in your bag.")

	data2 = {'digits': '4', 'complexity':'0', 'goldCoins': '30', 'silverCoins': ''}
	resp = app.request("/setup", method="POST", data=data2)
	assert_response(resp, contains="You have to have some amount of Silver coins in your bag.")

	data3 = {'digits': '4', 'complexity':'0', 'goldCoins': '', 'silverCoins': ''}
	resp = app.request("/setup", method="POST", data=data3)
	assert_response(resp, contains="You have to have some amount of Gold and Silver coins in your bag.")

	#test max/min Gold/Silver amounts in the bag

	data4 = {'digits': '4', 'complexity':'0', 'goldCoins': '101', 'silverCoins': '30'}
	resp = app.request("/setup", method="POST", data=data4)
	assert_response(resp, contains="You may wanto to set the the maximum number of Gold and Silver coins to be 100 for each bag. Otherwise, the game will be really easy.")

	data5 = {'digits': '4', 'complexity':'0', 'goldCoins': '30', 'silverCoins': '101'}
	resp = app.request("/setup", method="POST", data=data5)
	assert_response(resp, contains="You may wanto to set the the maximum number of Gold and Silver coins to be 100 for each bag. Otherwise, the game will be really easy.")

	data6 = {'digits': '4', 'complexity':'0', 'goldCoins': '10', 'silverCoins': '30'}
	resp = app.request("/setup", method="POST", data=data6)
	assert_response(resp, contains="You may wanto to set the the minimum number of Gold and Silver coins to be 20 for each bag. Otherwise, the game will be really challenging.")

	data7 = {'digits': '4', 'complexity':'0', 'goldCoins': '30', 'silverCoins': '10'}
	resp = app.request("/setup", method="POST", data=data7)
	assert_response(resp, contains="You may wanto to set the the minimum number of Gold and Silver coins to be 20 for each bag. Otherwise, the game will be really challenging.")


	# you have to test for the recommended Gold and Silver amounts, too.


def test_game():
#test the first GET request to /game
	a = code.Password('4', '0', '30', '30')
	password = a.create()
	session = 'web.session.Session object at 0x10c742520'
	resp = app.request("/game")
	assert_response(resp)

def test_game1():
	data1 = {'digits': '4', 'complexity':'0', 'goldCoins': '', 'silverCoins': '30'}
	resp = app.request("/setup", method="POST", data=data1)
	assert_response(resp, contains="You have to have some amount of Gold coins in your bag.")




# # def test_login():
# # 	#make sure default values work for the form
# # 	resp = app.request("/hello", method="POST")
# # 	assert_response(resp, contains="Nobody")




















