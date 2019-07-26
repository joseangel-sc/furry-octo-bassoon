from collections import Counter

import pandas as pd

from anagram.possible_words import PossibleWords


class Reduce:
    """
    Once we have a reduce list of possible words, the algorithm needs to keep looking for possible matches
    """
    def __init__(self, reduce_data_frame: pd.DataFrame, anagram: str) -> None:
        self.reduce_data_frame = reduce_data_frame
        self.anagram = anagram.replace(' ', '')
        self.anagram_counter = Counter(self.anagram)

