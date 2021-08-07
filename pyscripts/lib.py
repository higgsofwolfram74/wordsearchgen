import random
import math
import sys
from pathlib import Path
from dataclasses import dataclass, field
from typing import Tuple, List, Optional

import numpy as np


SHORTEST_WORD_LEN = 2


class InvalidWriteAttempt(Exception):
    pass


# holds dictionary and does word math
class Dictionary:

    # open document with words to use
    def __init__(self, path: Path):
        with path.open() as f:
            self.lexicon = [word for word in f.readlines()]

    # check if word exists
    def word_check(self, word: str):
        return word in self.lexicon

    # each word needs at least one space per letter and all letters surrounding each letter
    def word_bubble(word: str):
        if word.len() == SHORTEST_WORD_LEN:
            return 6 + SHORTEST_WORD_LEN
        elif word.len() > SHORTEST_WORD_LEN:
            return 6 + word.len() + (word.len() - 2) * 2
        else:
            print("Invalid word size...")
            return 0


# Holds the user's list of words
class Words:

    words: List[str]

    def __init__(self, words: List[str]):
        self.words = words

    # letters taken up by words
    def word_bubble(self):
        return sum(map(len, self.words))

    # method to take words from user by command line
    def get_word():
        user = ""
        words = []
        while user != "n":
            print("Write a word or 'n' to stop.")
            user = input().lower().strip()
            # smallest words I'll accept is two letter words
            if len(user) >= 2:
                words.append(user)

        return Words(words)

        
    def get_words():
        user = input("Write in the words you want and hit enter:\n")
        words = [word for word in user.lower().split(" ")]
        return Words(words)


    # list of words from a file
    def load_words(self, path: Path):
        with path.open() as f:
            return Words([word for word in f.readlines().strip()])

    # minimum number of elements for wordsearch
    def word_padding(self):
        padding = 0
        for word in self.wordlist:
            padding += Dictionary.word_bubble(word) + word.len()
        return padding

    # pick words to pad wordlist
    def random_words(self, dictionary: Dictionary, num_of_words=1000) -> List[str]:
        wordlist = []
        for i in range(num_of_words):
            wordlist.append(random.choice(dictionary.lexicon).strip())

        wordlist += self.words
        random.shuffle(wordlist)
        return wordlist


# holds data used by main logic code
class Mutate:

    word: str
    direction: Tuple[int]
    # if we find out that we can't place a word, we need to go back
    temp_ws_index: Tuple[int]
    blacklist: List[Tuple[int]] = []

    def __init__(self, word: str, index: Tuple[int]):
        self.word = word
        self.temp_ws_index = index

    def update(self, index: np.ndarray):
        self.temp_ws_index = index

    def orient(self, direction: Tuple[int]):
        self.direction = direction

    def black_list(self):
        self.blacklist.append(self.direction)

    def reset_blacklist(self):
        self.blacklist = []

    def pick_direction(self):
        directions = [
            (0, -1),  # up
            (1, -1),  # upright
            (1, 0),  # right
            (1, 1),  # downright
            (0, 1),  # down
            (-1, 1),  # downleft
            (-1, 0),  # left
            (-1, -1),  # upleft
        ]

        # filter out directions attempted and pick from remaining
        self.direction = random.choice(
            [x for x in filter(lambda k: k not in self.blacklist, directions)]
        )

    def go(self, width: int, length: int) -> bool:
        self.temp_ws_index = (
            self.temp_ws_index[0] + self.direction[0],
            self.temp_ws_index[1] + self.direction[1],
        )

        if self.temp_ws_index[0] < 0 or self.temp_ws_index[1] < 0:
            return False

        elif self.temp_ws_index[1] >= width:
            self.temp_ws_index[1] -= width
            self.temp_ws_index[0] += 1

        if self.temp_ws_index[0] >= length:
            return False

        return True


# bundle the functions related to placing words
class WordPlacer:
    def get(self, index: np.ndarray) -> Optional[str]:
        try:
            return self.wordsearch[index[0]][index[1]]
        except IndexError:
            return None

    def to_index(self, index: Tuple[int], offset: int) -> Optional[Tuple[int]]:
        temp = (index[0], index[1] + offset)

        while temp[1] >= self.width:
            temp = (temp[0] + 1, temp[1] - self.width)

        if temp[0] >= self.length:
            return None

        return temp

    # average out words across the
    def pick_location(self) -> int:
        top_dist = self.wordsearch.size // self.totalwords

        return random.randint(1, top_dist)

    def run_placer(self):
        index_holder = (0, 0)

        for word in self.wordlist.words:
            new_holder = self.to_index(index_holder, self.pick_location())

            # if run out of wordsearch, the wordsearch is malformed
            if index_holder is None:
                return None

            mutater = Mutate(word, new_holder)

            while not self.place_check(mutater):
                if len(mutater.black_list) == 8:
                    mutater.reset_blacklist()
                    mutater.update(self.to_index(index_holder, self.pick_location()))

            mutater.update(new_holder)

            try:
                self.place(mutater)
            # hopefully this never runs
            except InvalidWriteAttempt:
                print("Program attempted to write to occupied spaces")
                sys.exit(2)

        index_holder = new_holder

    def place_check(self, mutater: Mutate) -> bool:
        mutater.pick_direction()

        for character in mutater.word:
            getter = self.get(mutater.temp_ws_index)
            if getter != "_" and getter != character:
                mutater.black_list()
                return False

            if not mutater.go(self.width, self.length):
                mutater.black_list()
                return False

        return True

    def place(self, mutater: Mutate):
        for character in mutater.word:
            self.wordsearch[mutater.temp_ws_index] = character

            if not mutater.go(self.width, self.length):
                raise InvalidWriteAttempt


# main library for creating wordsearch
class WordsearchGenerator(WordPlacer):

    wordsearch: np.ndarray
    wordlist: Words

    def __init__(self, wordlist: Words, width: int = 500, length: int = 500) -> None:
        self.wordlist = wordlist
        self.totalwords = len(self.wordlist.words)
        self.numofletters = self.wordlist.word_bubble()

        if self.numofletters >= math.sqrt(width * length):
            self.width = width * self.numofletters
            self.length = length * self.numofletters
            self.wordsearch = np.array(
                [["_" for i in range(self.width)] for i in range(self.length)]
            )

        else:
            self.width = width
            self.length = length
            self.wordsearch = np.array(
                [["_" for i in range(self.width)] for i in range(self.length)]
            )

    def __str__(self):
        return f"{self.wordsearch}\nWordsearch with {self.wordsearch.size} elements created"

    # some vowels to make the wordsearch seem legit
    def random_vowels(self):
        vowels: str = "aeiouy"
        for _ in range(self.totalwords * self.numofletters):
            while True:
                location = (random.randint(0, self.length - 1), random.randint(0, self.width - 1))

                if self.wordsearch[location] == "_":
                    self.wordsearch[location] = random.choice(vowels)
                    break

    def fill_remaining(self):
        consonants = "bcdfghjklmnpqrstvwxz"
        with np.nditer(self.wordsearch, flags=["multi_index"]) as it:
            for elem in it:
                if elem == "_":
                    self.wordsearch[it.multi_index] = random.choice(consonants)

    # pick random spots to put words, a random direction, and throw the word down
    def generate_wordlist(self):
        self.run_placer()

        self.random_vowels()

        self.fill_remaining()

    def file_writer(self, wordlist: List[str], path: Path):
        wspath = path.joinpath("Wordsearch.txt")
        np.savetxt(wspath, self.wordsearch, fmt="%c", delimiter="", newline="\n")

        wlpath = path.joinpath("Wordlist.txt")
        with wlpath.open("w") as f:
            for word in wordlist:
                f.write(word + "\n")


if __name__ == "__main__":
    diction = Dictionary(Path("./Sources/myDict.txt"))
    words = Words.get_words()
    test = WordsearchGenerator(words, 500, 500)
    test.generate_wordlist()
    words_to_paste = words.random_words(diction)
    test.file_writer(words_to_paste, Path("./Output"))
