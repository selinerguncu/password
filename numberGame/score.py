from utils.rowToDict import rowToDict
from numberGame.constants import Constants


class Score(object):

    # multipliers = [
    #     1.0000000000000000000000000,
    #     0.1666666666666670000000000,
    #     0.0333333333333333000000000,
    #     0.0140468227424749000000000,
    #     0.0083333333333333300000000,
    #     0.0035650623885918000000000,
    #     0.0027777777777777800000000,
    #     0.0006384919428397690000000,
    #     0.0003764486550923640000000,
    #     0.0001114081996434940000000,
    #     0.0000304043782304652000000,
    #     0.0000064904940533166300000,
    #     0.0000035938128917256000000,
    #     0.0000015202189115232600000,
    #     0.0000001197937630575200000,
    #     0.0000001138683167248530000,
    #     0.0000000800115216591189000,
    #     0.0000000041308194157765600,
    #     0.0000000020333627986580900,
    #     0.0000000000369702327028744
    # ]

    multipliers = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
    def __init__(self, scoreVariables):

        self.scoreVariables = scoreVariables
        self.prob = self.findProb()


    def findProb(self):
        digits = self.scoreVariables["digits"]
        complexity = self.scoreVariables["complexity"]
        complexityRange = Constants["complexityRange"]

        prob = 1
        for i in range(digits):
            prob *= float(1)/(complexityRange[complexity]-i)

        return prob


    def findReward(self):
        norm = 1
        prob = self.prob
        rewardMultiplier = 1

        reward = norm / (rewardMultiplier * float(prob))

        return reward


    def coinsSpentCost(self):
        prob = self.prob
        weight_gold = 600
        weight_silver = 400

        cost_goldSpent = weight_gold * self.scoreVariables["goldSpent"] * float(prob)

        cost_silverSpent = weight_silver * self.scoreVariables["silverSpent"] * float(prob)

        cost_totalCoinsSpent = float(cost_goldSpent) + float(cost_silverSpent)

        return cost_totalCoinsSpent


    def findLevel(self):
        digits = self.scoreVariables["digits"]
        complexity = self.scoreVariables["complexity"]

        if digits == 4 and complexity == 0:
            level = 1
        elif digits == 5 and complexity == 0:
            level = 2
        elif digits == 6 and complexity == 0:
            level = 3
        elif digits == 6 and complexity == 1:
            level = 4
        elif digits == 7 and complexity == 0:
            level = 5
        elif digits == 8 and complexity == 2:
            level = 6
        elif digits == 8 and complexity == 0:
            level = 7
        elif digits == 7 and complexity == 1:
            level = 8
        elif digits == 10 and complexity == 3:
            level = 9
        elif digits == 9 and complexity == 2:
            level = 10
        elif digits == 8 and complexity == 1:
            level = 11
        elif digits == 11 and complexity == 3:
            level = 12
        elif digits == 10 and complexity == 2:
            level = 13
        elif digits == 9 and complexity == 1:
            level = 14
        elif digits == 11 and complexity == 2:
            level = 15
        elif digits == 12 and complexity == 3:
            level = 16
        elif digits == 10 and complexity == 1:
            level = 17
        elif digits == 12 and complexity == 2:
            level = 18
        elif digits == 13 and complexity == 3:
            level = 19
        elif digits == 14 and complexity == 3:
            level = 20
        return level


    def coinsInBagCost(self):
        level = self.findLevel()

        base_goldInBag = [20, 30, 37, 40, 42, 45, 47, 53, 55, 59, 64, 71, 73, 76, 93, 94, 96, 122, 125, 198]
        base_silverInBag = [20, 30, 37, 40, 42, 45, 47, 53, 55, 59, 64, 71, 73, 76, 93, 94, 96, 122, 125, 198]
        multiplier_CoinsInBag_forLevels = self.multipliers
        cost_baseGoldInBag = 0.06
        cost_baseSilverInBag = 0.04
        cost_additionalGold = 1.6
        cost_additionalSilver = 1.4

        baseCost_goldInBag = base_goldInBag[level - 1] * float(cost_baseGoldInBag)
        baseCost_silverInBag = base_silverInBag[level - 1] * float(cost_baseSilverInBag)
        # for custom games only:
        if self.scoreVariables["goldCoins"] >= base_goldInBag[level - 1]:
            cost_additionalGoldCoins = (self.scoreVariables["goldCoins"] - base_goldInBag[level - 1]) * float(cost_additionalGold)
            cost_additionalSilverCoins = (self.scoreVariables["silverCoins"] - base_silverInBag[level - 1]) * float(cost_additionalSilver)
        else: # eger defaulttan kucuk gold/silver tanimladiysa score u arttirmak icin multiplier i kucult:
            cost_additionalGoldCoins = ( 1 - (self.scoreVariables["goldCoins"] / base_goldInBag[level - 1])) * -1
            cost_additionalSilverCoins = ( 1 - (self.scoreVariables["silverCoins"] / base_silverInBag[level - 1])) * -1

        cost_goldCoinInBag = (baseCost_goldInBag + float(cost_additionalGoldCoins)) * multiplier_CoinsInBag_forLevels[level - 1]
        cost_silverCoinInBag = (baseCost_silverInBag + float(cost_additionalSilverCoins)) * multiplier_CoinsInBag_forLevels[level - 1]

        cost_totalCoinsInBag = float(cost_goldCoinInBag) + float(cost_silverCoinInBag)
        return cost_totalCoinsInBag


    def roundCost(self):
        level = self.findLevel()

        multiplier_additionalRounds_forLevels = self.multipliers

        multiplier_additionalRound = multiplier_additionalRounds_forLevels[level-1]
        cost_totalRounds = 0

        for rounds in range((self.scoreVariables["totalRounds"] + 1)):
            cost_eachRound = (10**(0.0175 * (rounds + 1) * multiplier_additionalRound)) - 1
            cost_totalRounds += float(cost_eachRound)

        return cost_totalRounds


    def calculateScore(self):

        # norm = 100
        norm = 1
        rewardMultiplier = 1

        prob = self.prob
        reward = self.findReward()
        cost_totalCoinsSpent = self.coinsSpentCost()
        cost_totalCoinsInBag = self.coinsInBagCost()
        cost_totalRounds = self.roundCost()

        totalCost = float(cost_totalCoinsSpent) + float(cost_totalCoinsInBag) + float(cost_totalRounds)

        costMultiplier = totalCost

        scoreMultiplier = rewardMultiplier + float(costMultiplier)

        score = norm / (float(prob) * float(scoreMultiplier))

        return score


    def getMaxScores(self):

        maxScores = []
        scoreVariables = {}

        scoreVariables["totalRounds"] = 1
        scoreVariables["goldSpent"] = 0
        scoreVariables["silverSpent"] = 0

        for level in Constants["levels"]:
            scoreVariables["digits"] = Constants["digits"][level-1]
            scoreVariables["complexity"] = Constants["complexity"][level-1]
            scoreVariables["goldCoins"] = Constants["goldCoins"][level-1]
            scoreVariables["silverCoins"] = Constants["silverCoins"][level-1]
            score = Score(scoreVariables)
            maxScores.append(score.calculateScore())

        return maxScores





















