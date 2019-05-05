from typing import List, Tuple
import nltk
# import gensim
import os
from gensim.models import FastText
from random import randint
import gensim.downloader as api

# # This was a workaround for utils-module not found -error,
# # there must be a better way to do it.
# import sys
# sys.path.append("..")

from roses.utils import read_json_file, get_path

# TODO where should these be run?
nltk.download('averaged_perceptron_tagger')

DEBUG = False


# TODO
# - evaluate similar words and pick a good replacement
# - make sure the return method returns the correct things - DONE
# - possibly make a way to save the model and reload it - STARTED, runs nicely here
#       but doesn't work from main.py yet 



def evaluate_replacement():
    return 0


def generate_word_pairs(emotion: str, word_pairs: List[Tuple[str, str]]):
    """
    Generates a bunch of word pairs depending on input word pairs and emotion.
    """
    print("Loading model into memory (will take a minute)")
    word_vec = api.load("glove-wiki-gigaword-100")
    print("LOADED")

    final_pairs = []

    if DEBUG:
        for p in final_pairs:
            print(p[0])
            print(p[1])
            print(type(p[0]))
            print("__________________")

    for pair in word_pairs:
        noun, adjc = find_alternative(pair, word_vec)
        
        changed_pair = [noun, adjc]
        final_pairs.append(changed_pair)

    # return method needs work such that it returns the correct thing - DONE
    return [{'word_pair': (word_pair[0], word_pair[1]), 'verb': 'is'} for word_pair in final_pairs]


def find_alternative(word, word_vec):
    tries = 20
    while True:
        similarword = word_vec.most_similar(positive=[word[0],word[1]], topn = tries)
        tagged = nltk.pos_tag([x[0] for x in similarword])
        nouns = [x[0] for x in tagged if x[1] in ['NN', 'NNS', 'NNP', 'NNPS']]
        adjc = [x[0] for x in tagged if x[1] in ['JJ', 'JJR', 'JJS']]
        if nouns:
            if adjc:
                idx_noun = randint(0,len(nouns)-1)
                idx_adjc = randint(0,len(adjc)-1)
                selectendNN = nouns[idx_noun]
                selectedJJ = adjc[idx_adjc]
                return selectendNN, selectedJJ
        tries += 5
        


# For testing
if __name__ == '__main__':
    example_emotion = 'sad'
    example_word_pairs = [("human", "brutal")]
    output = generate_word_pairs(example_emotion, example_word_pairs)
    print(output)
