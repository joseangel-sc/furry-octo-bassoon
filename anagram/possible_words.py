from collections import Counter

import pandas as pd


class PossibleWords:
    """
    This class gets a list of letters, in some random order, generates the possible
    anagrams and then delivers the anagram that matches the right hash to the answer
    """

    def __init__(self, anagram: Counter,
                 words_to_choose_from: pd.DataFrame = pd.read_csv('wordlist.txt', sep=" ", header=None)) -> None:
        self.anagram_counter = anagram
        self.letter_df = words_to_choose_from
        self.letter_df.columns = ['word']
        self.letter_df.dropna(inplace=True)
        self.letter_df.drop_duplicates(inplace=True)
        self.anagrams = []
        self.sums_values = []
        self.least_common = min(anagram, key=anagram.get)
        self.most_common = max(anagram, key=anagram.get)

    def __call__(self):
        self.get_possible_words()
        self.counter_columns()
        self.get_len_column()
        self.split_values()
        self.mixins()
        return self.letter_df

        # self.words_sum(list(self.letter_df['length'].unique()), len(self.anagram), [])

    def get_possible_words(self) -> None:
        self.letter_df['is_possible'] = self.letter_df['word'].apply(self.word_is_possible)
        self.letter_df = self.letter_df[self.letter_df['is_possible']]
        self.letter_df.drop(['is_possible'], inplace=True, axis=1)
        self.letter_df.reset_index(inplace=True, drop=True)

    def counter_columns(self) -> None:
        self.letter_df['counter'] = self.letter_df['word'].apply(PossibleWords.count_letters)

    def word_is_possible(self, word: str) -> bool:
        """
        :return: if a word is a possible anagram from some subset of letters from original
        list
        """
        word_counter = Counter(word)
        return self.anagram_counter & word_counter == word_counter

    @staticmethod
    def count_letters(word) -> dict:
        """
        Given a word, creates the corresponding dict of the Counter object
        :return: str
        """
        return dict(Counter(word))

    # def words_sum(self, numbers: list, target: int, partial: list) -> None:
    #     """
    #     from stackoverflow.com/questions/4632322/finding-all-possible-combinations-of-numbers-to-reach-a-given-sum
    #     This function will give us the possible sums that add to the right length of the original anagram
    #     """
    #     # def subset_sum(numbers, target, partial=[]):
    #     current_sum = sum(partial)
    #     if current_sum == target:
    #         self.sums_values.append(partial)
    #     if current_sum >= target:
    #         return None
    #     for i in range(len(numbers)):
    #         n = numbers[i]
    #         remaining = numbers[i + 1:]
    #         self.words_sum(remaining, target, partial + [n])
    #
    def get_len_column(self):
        self.letter_df['length'] = self.letter_df['word'].apply(len)

    def split_values(self):
        self.letter_df = pd.concat([self.letter_df.drop(['counter'], axis=1), self.letter_df['counter'].apply(pd.Series)], axis=1)
        self.letter_df.fillna(0, inplace=True)

    def mixins(self):
        mask_least = self.letter_df[self.least_common] > 0
        mask_most = self.letter_df[self.most_common] > 0
        #we know this can't go with each other
        least_common_df = self.letter_df[mask_least]
        most_common_df = self.letter_df[mask_most]
        most_common_that_dont_mix = pd.merge(most_common_df, least_common_df, how='inner')
        import ipdb
        ipdb.set_trace()
        most_common_that_mix = most_common_df[~most_common_df["word"].isin(most_common_that_dont_mix["word"])].copy()


"""
Can you write the algorithm to find it?

Here is a couple of important hints to help you out:
- An anagram of the phrase is: "poultry outwits ants"
- There are three levels of difficulty to try your skills with
- The MD5 hash of the easiest secret phrase is "e4820b45d2277f3844eac66c903e84be"
- The MD5 hash of the more difficult secret phrase is "23170acc097c24edb98fc5488ab033fe"
- The MD5 hash of the hard secret phrase is "665e5bcb0c20062fe8abaaf4628bb154"

"""

