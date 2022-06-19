from datetime import date
import hashlib
import os

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def hashDate(length):
    today = date.today().strftime("%d%m%Y").encode('utf-8')
    return int(hashlib.sha512(today).hexdigest(), 16) % length-1

def getWord():
    file = open('names.txt', 'r')
    lines = file.readlines()
    hashValue = hashDate(len(lines))
    word = lines[hashValue]
    file.close()
    return word[:-1]

def getLetterSet(word):
    letters = []
    for letter in word:
        if letter not in letters:
            letters.append(letter)
    return letters

def color(word, tried):
    gyw = ["\u001b[32m", "\u001b[33m", "\u001b[37m"] #green, yellow, white
    wordLetters = getLetterSet(word)

    colored = []
    for x in range(len(word)):
        colored.append("-")

    # Coloring green
    for i in range(len(word)):
        if word[i] == tried[i]:
            colored[i] = (gyw[0] + tried[i] + gyw[2])
            if tried[i] in wordLetters:
                wordLetters.remove(tried[i])

    # Coloring yellow
    for i in range(len(word)):
        if tried[i] in wordLetters and colored[i] == "-":
            colored[i] = (gyw[1] + tried[i] + gyw[2])
            if tried[i] in wordLetters:
                wordLetters.remove(tried[i])

    # Coloring white
    for i in range(len(word)):
        if colored[i] == "-":
            colored[i] = (gyw[2] + tried[i] + gyw[2])

    stringbuilder = ""
    for letter in colored:
        stringbuilder += letter
    return stringbuilder

def printOnTerminal(triedWords):
    clear()
    for word in triedWords:
        print(word)

def printResult(triedWords): #still prints 5x ⬛ eventho word has less or more letters <- to be fixed
    string = ""
    for i in range(1, len(triedWords)):
        farbenBuchstaben = []
        farbenBuchstaben.append(triedWords[i][2:4])
        farbenBuchstaben.append(triedWords[i][13:15])
        farbenBuchstaben.append(triedWords[i][24:26])
        farbenBuchstaben.append(triedWords[i][35:37])
        farbenBuchstaben.append(triedWords[i][46:48])
        for element in farbenBuchstaben:
            if element == "32":
                string += "🟩"
            elif element == "33":
                string += "🟨"
            else:
                string += "⬛"
        string += "\n"
    return string

def startGame(word, maxTries):
    won = False
    tries = 0
    triedWords = ["\u001b[31mWORDLE\u001b[37m"]

    while tries < maxTries and won == False:
        printOnTerminal(triedWords)
        tried = str(input())
        while len(tried) != len(word): # if length of input word is not length of the word to find
            printOnTerminal(triedWords)
            tried = str(input())
        coloredTried = color(word, tried)
        triedWords.append(coloredTried)
        if (tried == word):
            won = True
        tries+=1
    return [won, triedWords, tries]

todaysword = getWord()
MAX_TRIES = 6
results = startGame(todaysword, MAX_TRIES)

if results[0]:
    printOnTerminal(results[1])
    print("You won! [Tries: " + str(results[2]) + "]")
else:
    printOnTerminal(results[1])
    print("You lost...Come back tomorrow!")
print(printResult(results[1])[:-1])
