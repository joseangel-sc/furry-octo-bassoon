from collections import Counter
from typing import Tuple

import pandas as pd


class PossibleWords:
    """
    This class gets a list of letters, in some random order, generates the possible
    anagrams and then delivers the anagram that matches the right hash to the answer
    """

    def __init__(self, anagram: str,
                 words_to_choose_from: pd.DataFrame = pd.read_csv('wordlist.txt', sep=" ", header=None)) -> None:
        self.anagram_counter = Counter(sorted(anagram))
        self.letter_df = words_to_choose_from
        self.letter_df.columns = ['word']
        self.letter_df.dropna(inplace=True)
        self.letter_df.drop_duplicates(inplace=True)
        self.anagrams = []
        self.sums_values = []
        self.least_common = min(self.anagram_counter, key=self.anagram_counter.get)
        self.most_common = max(self.anagram_counter, key=self.anagram_counter.get)
        self.most_common_that_mix = pd.DataFrame()
        self.most_common_that_dont_mix = pd.DataFrame()

    def __call__(self):
        self.get_possible_words()
        self.counter_columns()
        self.get_len_column()
        self.split_values()
        self.one_appearance_vs_most_common_dfs()
        self.generate_groups_that_mix()
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
        self.letter_df = pd.concat(
            [self.letter_df.drop(['counter'], axis=1), self.letter_df['counter'].apply(pd.Series)], axis=1)
        self.letter_df.fillna(0, inplace=True)

    def one_appearance_vs_most_common_dfs(self) -> None:
        mask_most = self.letter_df[self.most_common] > 0
        mask_least = self.letter_df[self.least_common] > 0
        most_common_df = self.letter_df[mask_most]
        least_common_df = self.letter_df[mask_least]
        self.most_common_that_dont_mix = pd.merge(most_common_df, least_common_df, how='inner')
        self.most_common_that_mix = most_common_df[
            ~most_common_df["word"].isin(self.most_common_that_dont_mix["word"])].copy()

    def generate_groups_that_mix(self) -> dict:
        new_dfs = {}
        values_with_one = {k: v for k, v in self.anagram_counter.items() if v == 1 and v != self.least_common}
        do_mix = self.most_common_that_mix
        for letter in values_with_one:
            dont_mix, do_mix = PossibleWords._create_not_mixer_df(do_mix, letter)
            new_dfs[letter] = dont_mix
        import ipdb
        ipdb.set_trace()
        return new_dfs

    @staticmethod
    def _create_not_mixer_df(not_classified: pd.DataFrame, letter: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
        letter_mask = not_classified[letter] > 0
        contains_letter = not_classified[letter_mask]
        not_letter = not_classified[~letter_mask]
        return contains_letter, not_letter


"""
Can you write the algorithm to find it?

Here is a couple of important hints to help you out:
- An anagram of the phrase is: "poultry outwits ants"
- There are three levels of difficulty to try your skills with
- The MD5 hash of the easiest secret phrase is "e4820b45d2277f3844eac66c903e84be"
- The MD5 hash of the more difficult secret phrase is "23170acc097c24edb98fc5488ab033fe"
- The MD5 hash of the hard secret phrase is "665e5bcb0c20062fe8abaaf4628bb154"

"""
