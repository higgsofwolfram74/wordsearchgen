from dataclasses import dataclass, field
from abc import ABC, abstractclassmethod
from typing import List

import numpy as np
from nptyping import NDArray, Unicode



class Wordsearch:

    #get dimensions, and then make "empty" wordsearch
    def __init__(self, width=50, length=50):
        arr = [['_' for i in range(width)] for i in range(length)]
        self.wordsearch = np.array(arr)


    #see internal state
    def __str__(self):
        print(self.wordsearch)


@dataclass
class Words:
    
    words: List[str]
    
    def get_words(self):
        user = ''
        while user != 'n':
            print("Write a word or 'n' to stop.")
            user = input().lower().strip()
            #smallest words I'll accept is two letter words
            if user.len() >= 2:
                self.words.append(user)

    def load_words(self, path):
        with open(path, 'r') as f:
            self.words = [word for word in f.readlines().strip()]


@dataclass
class WordsearchGenerator:

    wordsearch: Wordsearch
    wordlist: Words


    #pick random spots to put words, a random direction, and throw the word down
    def generate_wordlist(self):
        pass




test = Wordsearch(200, 100)
print(test)