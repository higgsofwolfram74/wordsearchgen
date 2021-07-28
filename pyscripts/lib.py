import random
import math
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Set

import numpy as np
from nptyping import NDArray, Unicode


SHORTEST_WORD_LEN = 2


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


    def word_bubble(word: str):
        if word.len() == SHORTEST_WORD_LEN:
            return 6
        elif word.len() > SHORTEST_WORD_LEN:
            return 6 + (word.len() - 2) * 2
        else:
            print("Invalid word size...")
            return 0

class Wordsearch:

    #get dimensions, and then make "empty" wordsearch
    def __init__(self, width=50, length=50):
        arr = [['_' for i in range(width)] for i in range(length)]
        self.wordsearch = np.array(arr)
        


    #see internal state
    def __str__(self):
        return f"{self.wordsearch}"

    
    def __len__(self):
        return self.wordsearch.size

    
    
        


@dataclass
class Words:
    
    words: List[str]

    #letters taken up by words
    def word_bubble(self):
        return sum(map(lambda n: Words.by_len(n), self.words))


    def by_len(word: str):
        return word.len()
    

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
@dataclass
class Mutate:

    word: str
    index: int = (0, 0)
    blacklist: List[str] = []

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




#bundle the functions related to placing words
class WordPlacer():
    
    def pick_location(self) -> int:
        bottom_dist = 0
        top_dist = self.wordsearch.len() // self.numofletters

        i = 0

        #pick a random location between bottom_dist and top_dist so all words fit
        while random.randint(bottom_dist, top_dist) != bottom_dist:
            i += 1
            bottom_dist += 1

        return i

    
    def pick_direction(self, mutater: Mutate):
        directions = [
            mutater.go_up(),
            mutater.go_upleft(),
            mutater.go_left(),
            mutater.go_downleft(),
            mutater.go_down(),
            mutater.go_downright(),
            mutater.go_right(),
            mutater.go_upright()
        ]

        directions2 = [x for x in directions.filter(lambda k: k not in blacklist)]

        return directions2[random.choice(directions2)]

        

    
    def place_words(self, mutater: Mutate):

        

        for word in self.wordlist:
            while True:
                mutater.word = word



    
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