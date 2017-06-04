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


