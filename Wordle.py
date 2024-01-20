# -*- coding: utf-8 -*-
"""
Created on Tue Jan  4 16:24:40 2022

@author: Louis
"""

import ast
import random
import time
import math

simCount = 100
guessSampleCount = 50

#Game simulation

class wordleGame:
    def printSimulationResults(self):
        print('Average incorrect guesses was ' + str(self.guesses/self.simCount) + ', ' + str(self.losses) + ' losses, ' + str(self.simCount) + ' trials executed in ' + str(round(self.executionTime, 3)) + ' seconds')
    
    def __init__(self):
        words_file = open("Words.txt", "r")
        self.words = ast.literal_eval(words_file.read())
        words_file.close()
        
        self.maxGuesses = 6

        
    def simulate(self, simCount):
        self.guesses = 0
        self.losses = 0
        self.simCount = simCount
        
        start = time.perf_counter()
        
        for i in range(simCount):
            guesses = self.playWordle()
            self.guesses += guesses
            if guesses == self.maxGuesses:
                self.losses+=1
                
        end = time.perf_counter()  
        self.executionTime = end-start
        
    def playWordle(self):
        
        guesses = 0
        correctWord = random.choice(self.words)
        remainingWords = self.words
        
        print('correctWord = ' + correctWord)
    
        
        while guesses < self.maxGuesses:
            #print(len(remainingWords))
            
            # First guess is the same every time
            if guesses == 0:
                guess = self.makeFirstGuess()
            else:
                guess = self.strategicGuess(remainingWords)
            
            print(guess + ' ' + str(len(remainingWords)))
            
            if guess == correctWord:
                return guesses
            else:
                guesses += 1
                remainingWords = self.checkGuess(guess, correctWord, remainingWords)
                    
            
        return guesses
    
    def makeFirstGuess(self):
        return "soare"
    
    def checkGuess(self, guess, correctWord, remainingWords):
        # Logic for green, yellow and grey letters
        for idx, guessLetter in enumerate(list(guess)):
                    
            # Grey letters
            if guessLetter not in correctWord:
                remainingWords = [word for word in remainingWords if guessLetter not in word]
            # Green letters
            elif guessLetter == correctWord[idx]:
                remainingWords = [word for word in remainingWords if guessLetter == word[idx]]
                
            # Yellow letters
            else:                     
                remainingWords = [word for word in remainingWords if guessLetter in word if guessLetter is not word[idx]]
                
        return remainingWords
        
    
    def randomGuess(self, remainingWords):
        
        return random.choice(remainingWords)
    
    def strategicGuess(self, words):
        
        # If one word left or 50/50 just pick one
        if len(words) <= 2:
            return words[0]
        
        cumulativeGuessStrength = 0
        bestAverageGuessStrength = 0
        guess = words[0]
        sample = random.sample(words, min(guessSampleCount, len(words)))
        
        # Loop through all the possible words
        for testGuess in words:
            # Test each word against the random sample of possible correct answers      
            for correctWord in sample:
                remainingWords = self.checkGuess(testGuess, correctWord, words)
                guessStrength = self.evaluateGuessStrength(words, remainingWords)
                cumulativeGuessStrength += guessStrength
            # Check if it was the best performing so far on average   
            averageGuessStrength = cumulativeGuessStrength / len(sample)
            if averageGuessStrength > bestAverageGuessStrength:
                guess = testGuess
                bestGuessStrength = guessStrength           
                
        return guess
    
    def manualGuess(self, guess):
        
        return "tears"
    
    def evaluateGuessStrength(self, words, remainingWords):
        return self.bitsRemaining(words) - self.bitsRemaining(remainingWords)

    def bitsRemaining(self, words):
            return math.log2(len(words))
    
    def evaluateFirstGuess(self, guess):
        sumOfBits = 0
               
        for correctWord in self.words:
            remainingWords = self.checkGuess(guess, correctWord, self.words)
            sumOfBits += self.evaluateGuessStrength(self.words, remainingWords)
        
        averageBits = sumOfBits / len(self.words)
        
        return averageBits
    
    def evaluateAllFirstGuesses(self):
        
        for guess in self.words:
            averageBits =self.evaluateFirstGuess(guess)
            print(str(guess) + ', ' + str(averageBits) + ' average bits')
        
         
game = wordleGame()


#game.evaluateAllFirstGuesses()
#print(game.evaluateFirstGuess("soare"))

game.simulate(simCount)
game.printSimulationResults()