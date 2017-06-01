import random

class Password:
	def __init__(self, length, complexity, goldCoins, silverCoins):
		self.length = int(length)
		self.complexity = int(complexity)
		self.goldCoins = int(goldCoins)
		self.silverCoins = int(silverCoins)

	def create(self):
		self.onlyNumbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
		self.onlyLetters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'r', 's', 't', 'u', 'v', 'y', 'z', 'x', 'q', 'w']
		self.numbersLetters = self.onlyNumbers + self.onlyLetters

		if self.complexity == 0:
			password = random.sample(self.onlyNumbers, self.length)
		elif self.complexity == 1:
			password = random.sample(self.onlyLetters, self.length)
		elif self.complexity == 2:
			password = random.sample(self.numbersLetters, self.length)
		
		return password


	def drawBoxes(self):
		print ((('*' * 5) + '   ') * self.length)
		for i in range(3):
			print ((('*' + ' ' * 3 + '*') + '   ') * self.length)
		print ((('*' * 5) + '   ') * self.length)

	def evaluate(self, password, guess):

		self.goldCoinsReceived = 0
		self.silverCoinsReceived = 0

		for i in range(self.length):
			if guess[i] == password[i]:
				self.goldCoinsReceived += 1
			elif guess[i] in password:
				self.silverCoinsReceived += 1
		

		self.evaluation = {}
		self.evaluation["guess"] = guess
		self.evaluation["goldCoinsReceived"] = self.goldCoinsReceived
		self.evaluation["silverCoinsReceived"] = self.silverCoinsReceived 

		return self.evaluation

	def update(self, goldCoins, silverCoins, round_, evaluation):
		guess = evaluation["guess"]
		# round_ = evaluation["round"]
		goldCoinsReceived = int(evaluation["goldCoinsReceived"])
		silverCoinsReceived = int(evaluation["silverCoinsReceived"])
		round_ = int(round_)
		self.goldCoinsInBag = int(goldCoins)
		self.silverCoinsInBag = int(silverCoins)
		
		if self.goldCoinsInBag == 0:
			goldCoinsReceived = '**'

		if self.silverCoinsInBag == 0:
			silverCoinsReceived = '**'

		if goldCoinsReceived != '**':
			self.goldCoinsInBag = self.goldCoins - goldCoinsReceived
			if self.goldCoinsInBag <= 0:
				self.goldCoinsInBag = 0

		if silverCoinsReceived != '**':
			self.silverCoinsInBag = self.silverCoins - silverCoinsReceived
			if self.silverCoinsInBag <= 0:
				self.silverCoinsInBag = 0

		round_ += 1

		updated = {}
		updated["round"] = round_
		updated["guess"] = guess
		updated["goldCoinsReceived"] = goldCoinsReceived
		updated["silverCoinsReceived"] = silverCoinsReceived
		updated["goldCoinsInBag"] = self.goldCoinsInBag
		updated["silverCoinsInBag"] = self.silverCoinsInBag

		return updated


class Score:
	def __init__(self, length, complexity, goldCoinsSpent, silverCoinsSpent, round_):
		self.length = int(length)
		self.complexity = int(complexity)
		self.goldCoinsSpent = int(goldCoinsSpent)
		self.silverCoinsSpent = int(silverCoinsSpent)
		self.round = round_

		print self.length, self.complexity

	def score(self):
		if self.length == 4 and self.complexity == 0:
			prob = float(((float(1))/10) * ((float(1))/9) * ((float(1))/8) * ((float(1))/7))
		elif self.length == 5 and self.complexity == 0:
			prob = float(((float(1))/10) * ((float(1))/9) * ((float(1))/8) * ((float(1))/7) * ((float(1))/6))
		elif self.length == 6 and self.complexity == 0:
			prob = float(((float(1))/10) * ((float(1))/9) * ((float(1))/8) * ((float(1))/7) * ((float(1))/6) * ((float(1))/5))
		elif self.length == 7 and self.complexity == 0:
			prob = float(((float(1))/10) * ((float(1))/9) * ((float(1))/8) * ((float(1))/7) * ((float(1))/6) * ((float(1))/5) * ((float(1))/4))
		elif self.length == 8 and self.complexity == 0:
			prob = float(((float(1))/10) * ((float(1))/9) * ((float(1))/8) * ((float(1))/7) * ((float(1))/6) * ((float(1))/5) * ((float(1))/4) * ((float(1))/3))
		elif self.length == 4 and self.complexity == 1:
			prob = float(((float(1))/26) * ((float(1))/25) * ((float(1))/24) * ((float(1))/23))
		elif self.length == 5 and self.complexity == 1:
			prob = float(((float(1))/26) * ((float(1))/25) * ((float(1))/24) * ((float(1))/23) * ((float(1))/22))
		elif self.length == 6 and self.complexity == 1:
			prob = float(((float(1))/26) * ((float(1))/25) * ((float(1))/24) * ((float(1))/23) * ((float(1))/22) * ((float(1))/21))
		elif self.length == 7 and self.complexity == 1:
			prob = float(((float(1))/26) * ((float(1))/25) * ((float(1))/24) * ((float(1))/23) * ((float(1))/22) * ((float(1))/21) * ((float(1))/20))
		elif self.length == 8 and self.complexity == 1:
			prob = float(((float(1))/26) * ((float(1))/25) * ((float(1))/24) * ((float(1))/23) * ((float(1))/22) * ((float(1))/21) * ((float(1))/20) * ((float(1))/19))
		elif self.length == 4 and self.complexity == 2:
			prob = float(((float(1))/36) * ((float(1))/35) * ((float(1))/34) * ((float(1))/33))
		elif self.length == 5 and self.complexity == 2:
			prob = float(((float(1))/36) * ((float(1))/35) * ((float(1))/34) * ((float(1))/33) * ((float(1))/32))
		elif self.length == 6 and self.complexity == 2:
			prob = float(((float(1))/36) * ((float(1))/35) * ((float(1))/34) * ((float(1))/33) * ((float(1))/32) * ((float(1))/31))
		elif self.length == 7 and self.complexity == 2:
			prob = float(((float(1))/36) * ((float(1))/35) * ((float(1))/34) * ((float(1))/33) * ((float(1))/32) * ((float(1))/31) * ((float(1))/30))
		elif self.length == 8 and self.complexity == 2:
			prob = float(((float(1))/36) * ((float(1))/35) * ((float(1))/34) * ((float(1))/33) * ((float(1))/32) * ((float(1))/31) * ((float(1))/30) * ((float(1))/29))


		weightGold = 0.6
		weightSilver = 0.4

		norm = 0.1

		print "prob", prob
		print "coins", self.goldCoinsSpent

		if self.round == 1:
			self.goldCoinsSpent = 0
			score = int(norm / (prob * weightGold * self.goldCoinsSpent + prob * weightSilver * 1))
		else:
			score = int(norm / ((prob * weightGold * self.goldCoinsSpent) + (prob * weightSilver * self.silverCoinsSpent) )) - (1 * self.round)
		print "goldCoinsSpent", self.goldCoinsSpent
		print "silverCoinsSpent", self.silverCoinsSpent
		print "self.length", self.length
		print "self.round", self.round
		print "self.complexity", self.complexity
		print "self.goldCoinsSpent", self.goldCoinsSpent
		print "self.silverCoinsSpent", self.silverCoinsSpent

		# return "{:,}".format(score) #will be a string
		return score # will be a string





























	 