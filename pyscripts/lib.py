import random
from dataclasses import dataclass, field
from typing import List

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


    def word_bubble(word: str, n: int):
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


@dataclass
class Words:
    
    words: List[str]

    #every word needs a letter buffer around it. Returns lowest possible size
    def word_bubble(word: str, n: int):
        if word.len() == SHORTEST_WORD_LEN:
            return 6
        elif word.len() > SHORTEST_WORD_LEN:
            return 6 + (word.len() - 2) * 2
        else:
            print("Invalid word size...")
            return 0


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

    



class WordsearchGenerator:

    wordsearch: Wordsearch
    wordlist: Words

    def __init__(self, wordlist: Words):
        self.wordlist = wordlist


    #pick random spots to put words, a random direction, and throw the word down
    def generate_wordlist(self):
        pass




test = Wordsearch(200, 100)
print(test)