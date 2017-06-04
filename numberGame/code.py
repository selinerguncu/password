import random
from numberGame.constants import Constants

class Password:
    def __init__(self, length, complexity, goldCoins, silverCoins):
        self.length = int(length)
        self.complexity = int(complexity)
        self.goldCoins = int(goldCoins)
        self.silverCoins = int(silverCoins)

    def create(self):
        onlyNumbers = Constants["onlyNumbers"]
        onlyLetters = Constants["onlyLetters"]
        numbersLetters = Constants["numbersLowercaseLetters"]
        uppercaseLetters = Constants["uppercaseLetters"]
        numbersAllLetters = Constants["numbersAllLetters"]

        if self.complexity == 0:
            password = random.sample(onlyNumbers, self.length)
        elif self.complexity == 1:
            password = random.sample(onlyLetters, self.length)
        elif self.complexity == 2:
            password = random.sample(numbersLetters, self.length)
        elif self.complexity == 3:
            password = random.sample(numbersAllLetters, self.length)

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

