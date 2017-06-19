onlyNumbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
onlyLetters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'r', 's', 't', 'u', 'v', 'y', 'z', 'x', 'q', 'w']
numbersLowercaseLetters = onlyNumbers + onlyLetters
uppercaseLetters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbersAllLetters = numbersLowercaseLetters + uppercaseLetters

howToPlayLevels = {
    'level' : [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
    'digit' : [4, 5, 6, 7, 8, 6, 7, 8, 9, 8, 10, 9, 10, 11, 10, 12, 11, 12, 13, 14],
    'complexity' : ['Only Numbers', 'Only Numbers', 'Only Numbers', 'Only Numbers', 'Only Numbers',
    'Only Small Letters', 'Only Small Letters', 'Only Small Letters', 'Only Small Letters',
    'Small and Capital Letters', 'Only Small Letters', 'Small and Capital Letters',
    'Small and Capital Letters', 'Small and Capital Letters', 'Numbers, Small and Capital Letters',
    'Small and Capital Letters', 'Numbers, Small and Capital Letters', 'Numbers, Small and Capital Letters',
    'Numbers, Small and Capital Letters', 'Numbers, Small and Capital Letters'],
    'gold' : [20, 30, 37, 42, 46, 56, 65, 73, 81, 82, 89, 90, 102, 113, 120, 121, 136, 159, 181, 203],
    'silver' : [20, 30, 37, 42, 46, 56, 65, 73, 81, 82, 89, 90, 102, 113, 120, 121, 136, 159, 181, 203],
    'difficulty' : [1, 6, 5, 4, 3, 91, 20, 19, 19, 1, 17, 2, 27, 26, 16, 2, 34, 51, 50, 49],
    'maxScore' : ['2,000','10,000','20,000','50,000','80,000','110,000','140,000','170,000',
    '200,000','230,000','250,000','290,000','360,000','430,000','500,000','550,000','650,000',
    '750,000','850,000','1,000,000 '],
    'badge' : ['-', '-', '-', 'Ruby', 'Ruby', 'Ruby', 'Ruby', 'Ruby',
    'Sapphire', 'Sapphire', 'Sapphire', 'Sapphire', 'Sapphire', 'Sapphire', 'Emerald',
    'Emerald', 'Emerald', 'Emerald', 'Diamond', 'Diamond']}

howToPlayRecommended = {
    'onlyNumbers' : [(4, 20), (5, 30), (6, 37), (7, 42), (8, 46), (9, 48), (10,50)],
    'onlyLetters' : [(4, 52), (5, 54), (6, 56), (7, 65), (8, 73), (9, 81), (10,89), (11,93), (12,96), (13,99), (14,102)],
    'smallCapitalLetters' : [(4, 56), (5, 58), (6, 66), (7, 75), (8, 82), (9, 90), (10,102), (11,113), (12,125), (13,132), (14,145)],
    'numbersSmallCapitalLetters' : [(4, 65), (5, 74), (6, 80), (7, 88), (8, 100), (9, 112), (10,120), (11,136), (12,159), (13,181), (14,203)]
}


Constants = {
    "onlyNumbers" : onlyNumbers,
    "onlyLetters" : onlyLetters,
    "numbersLowercaseLetters" : numbersLowercaseLetters,
    "uppercaseLetters" : uppercaseLetters,
    "numbersAllLetters" : numbersAllLetters,
    "levels" : [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],


    "digits" :     [4, 5, 6, 7, 8, 6, 7, 8, 8, 9, 10, 9, 10, 11, 10, 12, 11, 12, 13, 14],
    "complexity" : [0, 0, 0, 0, 0, 1, 1, 1, 2, 1, 1,  2, 2,  2,  3,  2,  3,  3,  3,  3],

    "goldCoins" : [20, 30, 37, 42, 46, 56, 65, 73, 81, 82, 89, 90, 102, 113, 120, 125, 136, 159, 181, 203],
    "silverCoins" : [20, 30, 37, 42, 46, 56, 65, 73, 81, 82, 89, 90, 102, 113, 120, 125, 136, 159, 181, 203],
    "complexityRange" : [10, 26, 36, 62],
    "digitRange" : range(4, 15),
    "howToPlayLevels" : howToPlayLevels,
    "howToPlayRecommended" : howToPlayRecommended
}

