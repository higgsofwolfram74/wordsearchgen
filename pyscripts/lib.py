import random
import math
import sys
from abc import ABC, abstractmethod
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Callable, List, Tuple

import numpy as np
from nptyping import NDArray, Unicode


SHORTEST_WORD_LEN = 2

#holds dictionary and does word math
class Dictionary:

    #open document with words to use
    def __init__(self, path):
        with open(path, 'r') as f:
            self.lexicon = set([word for word in f.readlines()])

    
    #pick words to pad wordlist
    def random_words(self, num_of_words=1000):
        wordlist = []
        for i in range(num_of_words):
            wordlist.append(random.choic(self.lexicon))

        return wordlist

    
    #check if word exists
    def word_check(self, word: str):
        return word in self.lexicon


    #each word needs at least one space per letter and all letters surrounding each letter
    def word_bubble(word: str):
        if word.len() == SHORTEST_WORD_LEN:
            return 6 + SHORTEST_WORD_LEN
        elif word.len() > SHORTEST_WORD_LEN:
            return 6 + word.len() + (word.len() - 2) * 2
        else:
            print("Invalid word size...")
            return 0
     


#Holds the user's list of words
@dataclass
class Words:
    
    words: List[str] = []

    #letters taken up by words
    def word_bubble(self):
        return sum(map(len, self.words))


    

    #method to take words from user by command line
    def get_words(self):
        user = ''
        while user != 'n':
            print("Write a word or 'n' to stop.")
            user = input().lower().strip()
            #smallest words I'll accept is two letter words
            if user.len() >= 2:
                self.words.append(user)
        
        if self.words:
            self.words.sort(reverse=True, key = len)


    #list of words from a file
    def load_words(self, path):
        with open(path, 'r') as f:
            self.words = [word for word in f.readlines().strip()].sorted(reverse=True, key=len)

    
    #minimum number of elements for wordsearch
    def word_padding(self):
        padding = 0
        for word in self.wordlist:
            padding += Dictionary.word_bubble(word) + word.len()
        return padding


#holds data used by main logic code
class Mutate:

    word: str
    ws_width: int
    ws_index: int = (0, 0)
    #if we find out that we can't place a word, we need to go back
    temp_ws_index: int = (0, 0)
    blacklist: List[Tuple[int, int]] = []


    def put_word(self, word: str):
        self.word = word


    def update_location(self, location: Tuple[int, int]):
        self.ws_index = (self.ws_index[0] + location[0], self.ws_index[1] + location[1])
        self.temp_ws_index = self.ws_index


    def black_list(self, wrong_direction: Tuple[int, int]):
        self.blacklist.append(wrong_direction)


    def reset_index(self):
        self.temp_ws_index = self.ws_index


    def reset_blacklist(self):
        self.blacklist = []

    def go(self, move: Tuple[int, int]) -> None:
        self.temp_ws_index = (self.temp_ws_index[0] + move[0], self.temp_ws_index[1] + move[1])


    def to_index(n: int, width: int) -> Tuple[int, int]:
        if n < width:
            return (n, 0)
        else:
            return (n % width, n // width)


    def from_index(self, width: int) -> int:
        return self.ws_index[0] + self.ws_index[1] * width 



#bundle the functions related to placing words
class WordPlacer():
    
    def pick_location(self) -> int:
        bottom_dist = 0
        top_dist = len(self.wordsearch) // self.numofletters

        return random.randint(bottom_dist, top_dist)

    
    def pick_direction(self, mutater: Mutate) -> Tuple[int, int]:
        directions = [
            (0, -1),  #up
            (1, -1),  #upright
            (1, 0),   #right
            (1, 1),   #downright
            (0, 1),   #down
            (-1, 1),  #downleft
            (-1, 0),  #left
            (-1, -1), #upleft
        ]

        #filter out directions attempted and pick from remaining
        return random.choice([x for x in filter(lambda k: k not in mutater.blacklist, directions)])

            
    def place_words(self):    
        for word in self.wordlist:
            mutater = Mutate()

            mutater.put_word(word)

            spot = self.pick_location(mutater.from_index(self.width))
            mutater.update_location(Mutate.to_index(spot, self.width))
            
            #runs until word is placed
            while True:                
                direction_to = self.pick_direction(mutater)
                result = self.place(mutater, direction_to)
                
                if result is False:
                    mutater.black_list(direction_to)
                    
                    #should never be a situation where no direction is valid but here for sanity sake to try elsewhere
                    if len(mutater.blacklist) == 8:
                        mutater.reset_blacklist()

                        spot = self.pick_location(mutater.from_index(self.width))
                        mutater.update_location(Mutate.to_index(spot, self.width))
                        
                else:
                    break


    
    def place(self, mutater: Mutate, where_to: Tuple[int, int]) -> bool:
        """Returns true if word can and is placed. Otherwise, return false"""
        for letter in mutater.word:
            getter = self.wordsearch[mutater.temp_ws_index[0]][mutater.temp_ws_index[1]] 
            
            if getter != '_' and getter != letter:
                return False

            mutater.go(where_to)

        mutater.reset_index()

        for letter in mutater.word:
            if getter == '_':
                self.wordsearch[mutater.temp_ws_index[0]][mutater.temp_ws_index[1]] = letter
            elif getter == letter:
                pass
            else:
                print("Invalid locations written to")
                sys.exit(2)

            mutater.go(where_to)

        return True
            


    
#main library for creating wordsearch
class WordsearchGenerator(WordPlacer):

    wordsearch: NDArray[str]
    wordlist: Words

    def __init__(self, wordlist: Words, width: int = 500, length: int = 500) -> None:
        self.wordlist = wordlist
        self.totalwords = self.wordlist.len()
        self.numofletters = self.wordlist.word_bubble()

        if self.numofletters >= math.sqrt(width * length):
            self.width = width * self.numofletters
            self.wordsearch = np.array([['_' for i in range(self.width)] for i in range(self.numofletters * length)])
               
        else:
            self.width = width
            self.wordsearch = np.array([['_' for i in range(self.width)] for i in range(length)])
            


    #pick random spots to put words, a random direction, and throw the word down
    def generate_wordlist(self):
        pass


words = Words.get_words()
test = WordsearchGenerator(words, 200, 100)
print(test)