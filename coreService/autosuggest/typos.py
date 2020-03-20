import regex as re
from .regex_typo_fix import correct, create_dictionary
import os


# Build default dictionary
default_dictionary = create_dictionary("autosuggest/typos")
dictionary = default_dictionary


def get_possible_typos(word : str) -> str:
    # if len(word) == 1: return "."
    pattern = word # word as is
    pattern += f"|{correct(word, dictionary)}" # try to correct common typos
    pattern += "|" + ".?".join(word) + ".?" # missed letters at any position
    for i in range(len(word)):
        pattern += f"|{word[:i]}.{word[i+1:]}" # wrong symbol at any position
        pattern += f"|{word[:i]}.{word[i:]}" # missed 1 letter at any position
    if len(word) > 2:
        for i in range(len(word)): # 2 wrong symbols in word
            for j in range(i + 1, len(word)):
                tmp = list(word)
                tmp[i] = ".?"
                tmp[j] = ".?"
                pattern += "|" + "".join(tmp)
    if len(word) > 5:
        for i in range(len(word)-2):
            pattern += f"|{word[:i]}...{word[i+3:]}" # 3 wrong symbols in a row at any position

    return f"({pattern})"

if __name__ == "__main__":
    print(get_possible_typos(input()))