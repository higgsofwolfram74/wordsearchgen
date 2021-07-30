import random
import math
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

#factory of default wordsearches to fill
class Wordsearch:

    #get dimensions, and then make "empty" wordsearch
    def __init__(self, width=50, length=50):
        arr = [['_' for i in range(width)] for i in range(length)]
        self.wordsearch = np.array(arr)
        
    #see internal state
    def __str__(self):
        return f"{self.wordsearch}"

    #return number of elements of wordsearch
    def __len__(self):
        return self.wordsearch.size       


#Holds the user's list of words
@dataclass
class Words:
    
    words: List[str]

    #letters taken up by words
    def word_bubble(self):
        return sum(map(Words.by_len, self.words))

    
    #len of each word
    def by_len(word: str):
        return len(word)
    

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
            self.words.sort(reverse=True, key = Words.by_len())


    #list of words from a file
    def load_words(self, path):
        with open(path, 'r') as f:
            self.words = [word for word in f.readlines().strip()].sorted(reverse=True, key=Words.by_len())

    
    #minimum number of elements for wordsearch
    def word_padding(self):
        padding = 0
        for word in self.wordlist:
            padding += Dictionary.word_bubble(word) + word.len()
        return padding


#holds data used by main logic code
class Mutate:

    word: str
    word_index: int = 0
    ws_index: int = (0, 0)
    #if we find out that we can't place a word, we need to go back
    temp_ws_index: int = (0, 0)
    blacklist: List[str] = []

    #suite of functions to return index based on direction

    def go_up(self):
        return (self.index[0], self.index[1] - 1)
    
    def go_upleft(self):
        return (self.index[0], self.index[1] - 1)

    def go_left(self):
        return (self.index[0], self.index[1] - 1)

    def go_downleft(self):
        return (self.index[0], self.index[1] - 1)

    def go_down(self):
        return (self.index[0], self.index[1] - 1)

    def go_downright(self):
        return (self.index[0], self.index[1] - 1)

    def go_right(self):
        return (self.index[0], self.index[1] - 1)

    def go_upright(self):
        return (self.index[0], self.index[1] - 1)


    def to_index(n: int, width: int, length: int) -> Tuple[int, int]:
        if n < width:
            return (n, 0)
        else:
            return (n % width, n // length)


    def from_index(location: Tuple[int, int], width: int) -> int:
        return location[0] + location[1] * width



#bundle the functions related to placing words
class WordPlacer():


    
    def pick_location(self, start = 0) -> int:
        bottom_dist = 0
        top_dist = self.wordsearch.len() // self.numofletters

        i = 0

        #pick a random location between bottom_dist and top_dist so all words fit
        while random.randint(bottom_dist, top_dist) != bottom_dist:
            i += 1
            bottom_dist += 1

        return start + i

    
    def pick_direction(self, mutater: Mutate):
        directions = [
            mutater.go_up,
            mutater.go_upleft,
            mutater.go_left,
            mutater.go_downleft,
            mutater.go_down,
            mutater.go_downright,
            mutater.go_right,
            mutater.go_upright
        ]

        directions2 = [x for x in directions.filter(lambda k: k not in mutater.blacklist)]

        return directions2[random.choice(directions2)]

            
    def place_words(self):    
        for word in self.wordlist:
            mutater = Mutate()
            index = (0, 0)
            while True:
                mutater.word = word
                
                direction_to = self.pick_direction(mutater)

    
    def place(self, mutater: Mutate, where_to: Callable[[], int]):
        """First go across planned word location"""
        pass





    
#main library for creating wordsearch
class WordsearchGenerator(WordPlacer):

    wordsearch: Wordsearch
    wordlist: Words

    def __init__(self, wordlist: Words, width: int = 500, length: int = 500) -> None:
        self.wordlist = wordlist
        self.totalwords = self.wordlist.len()
        self.numofletters = self.wordlist.word_bubble()

        if self.numofletters >= math.sqrt(width * length):
            self.width = width * self.numofletters
            self.length = length * self.numofletters
            self.wordsearch = Wordsearch(self.width, self.length)
            
        else:
            self.wordsearch = Wordsearch(width, length)
            self.width = width
            self.length = length


    #pick random spots to put words, a random direction, and throw the word down
    def generate_wordlist(self):
        pass



test = Wordsearch(200, 100)
print(test)