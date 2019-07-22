from collections import Counter

import pandas as pd


class DecodeAnagram:
    """
    This class gets a list of letters, in some random order, generates the possible
    anagrams and then delivers the anagram that matches the right hash to the answer
    """

    def __init__(self, anagram: str, desire_hashes: list) -> None:
        self.anagram = anagram.replace(' ', '')
        self.anagram_counter = Counter(self.anagram)
        self.desire_hashes = desire_hashes
        self.letter_df = pd.read_csv('wordlist.txt', sep=" ", header=None)
        self.letter_df.columns = ['word']
        self.letter_df.dropna(inplace=True)
        self.letter_df.drop_duplicates(inplace=True)
        self.anagrams = []

    def __call__(self):
        self.get_possible_words()
        self.get_len_column()

    def get_possible_words(self) -> None:
        self.letter_df['is_possible'] = self.letter_df['word'].apply(self.word_is_possible)
        self.letter_df = self.letter_df[self.letter_df['is_possible']]
        self.letter_df.drop(['is_possible'], inplace=True, axis=1)
        self.letter_df.reset_index(inplace=True, drop=True)

    def word_is_possible(self, word: str) -> bool:
        """
        :return: if a word is a possible anagram from some subset of letters from original
        list
        """
        word_counter = Counter(word)
        return self.anagram_counter & word_counter == word_counter

    def get_len_column(self):
        self.letter_df['length'] = self.letter_df['word'].apply(len)

    def possible_new_words(self, word: str) -> None:
        remaining_anagram = self.anagram_counter - Counter(word)

        pass


"""
Can you write the algorithm to find it?

Here is a couple of important hints to help you out:
- An anagram of the phrase is: "poultry outwits ants"
- There are three levels of difficulty to try your skills with
- The MD5 hash of the easiest secret phrase is "e4820b45d2277f3844eac66c903e84be"
- The MD5 hash of the more difficult secret phrase is "23170acc097c24edb98fc5488ab033fe"
- The MD5 hash of the hard secret phrase is "665e5bcb0c20062fe8abaaf4628bb154"

"""