from collections import Counter, defaultdict
from functools import lru_cache
from string import ascii_uppercase

def readstrings():
    strings = []
    s = input()
    while s != "#":
        strings.append(s)
        s = input()
    return strings

def convert_string_to_tuple(s):
    counter = Counter(s)
    return tuple(counter.get(letter, 0) for letter in ascii_uppercase)

def lt(t1, t2):
    return all(e1 <= e2 for (e1, e2) in zip(t1, t2))

def minus(t1, t2):
    return tuple(e1 - e2 for (e1, e2) in zip(t1, t2))

def null(t):
    return all(e == 0 for e in t)

@lru_cache(maxsize=None)
def solve_rec(sentence_, i):
    if null(sentence_):
        return [tuple()]

    while i < len(words_) and not lt(words_[i], sentence_):
        i += 1

    if i == len(words_):
        return []

    next_sentence_ = minus(sentence_, words_[i])
    anagrams_with_word = [
        (i,) + e
        for e in solve_rec(next_sentence_, i + 1)
    ]
    anagrams_without_word = solve_rec(sentence_, i + 1)
    return anagrams_with_word + anagrams_without_word



words = sorted(readstrings())
sentences = readstrings()
words_ = list(map(convert_string_to_tuple, words))

for sentence in sentences:
    sentence_ = convert_string_to_tuple(sentence)
    anagrams_ = sorted(solve_rec(sentence_, 0))
    words_sentence = sentence.split(" ")
    for anagram_ in anagrams_:
        if all(words[i] not in words_sentence for i in anagram_):
            anagram = " ".join(words[i] for i in anagram_)
            print(sentence, "=", anagram)

