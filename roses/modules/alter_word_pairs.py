from typing import List, Tuple
import nltk
import os
from gensim.models import FastText
from random import randint
import gensim.downloader as api

from roses.utils import read_json_file, get_path
nltk.download('abc')
nltk.download('brown')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

from nltk.corpus import abc
from nltk.corpus import brown

DEBUG = False


# TODO
# - evaluate similar words and pick a good replacement
# - make sure the return method returns the correct things - DONE
# - possibly make a way to save the model and reload it - STARTED, runs nicely here
#       but doesn't work from main.py yet 


def train_model():
    data = read_json_file("data/bible_kjv_wrangled.json")
    sentences = list(data.values())
    # Do we want everything in lowercase?
    sentences = [s.lower() for s in sentences]

    print("-----------Tokenize corpus-------------")
    tokenized_sentences = []
    for s in sentences:
        tokens = nltk.word_tokenize(s)
        tokenized_sentences.append(tokens)

    for s in abc.sents():
        s = list(filter(lambda x: x.isalpha() and len(x) > 1, s))
        s = [x.lower() for x in s]  # Do we want everything in lowercase?
        tokenized_sentences.append(s)

    for s in brown.sents():
        s = list(filter(lambda x: x.isalpha() and len(x) > 1, s))
        s = [x.lower() for x in s]  # Do we want everything in lowercase?
        tokenized_sentences.append(s)

    print("------------TRAINING FASTTEXT-----------")

    model = FastText(tokenized_sentences, size=100, window=5, min_count=5, workers=4, sg=1)

    print("----------------DONE-------------")
    return model



# unused, evaluation moved to evaluation module
def evaluate_replacement():
    return 0

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

def generate_word_pairs(emotion: str, word_pairs: List[Tuple[str, str]]):
    """
    Generates a bunch of word pairs depending on input word pairs.
    """
    model_name = 'bible_model'
    model_dir = get_path('data/' + model_name)

    exists = os.path.isfile(model_dir)
    if exists:
        print('Found a pretrained FastText Bible model')
        model = FastText.load(model_dir)
    else:
        model = train_model()
        model.save(model_dir)
    print(model)

    print("Loading pretrained model into memory (will take a minute)")
    word_vec = api.load("glove-wiki-gigaword-100")
    print("LOADED")

    final_pairs = []

    for pair in word_pairs:
        noun, adjc = find_alternative(pair, word_vec)
        changed_pair = [noun, adjc]
        final_pairs.append(changed_pair)

    # return method needs work such that it returns the correct thing - DONE
    return [{'word_pair': (word_pair[0], word_pair[1]), 'verb': 'is'} for word_pair in final_pairs]



        


# For testing
if __name__ == '__main__':
    example_emotion = 'sad'
    example_word_pairs = [("human", "brutal")]
    output = generate_word_pairs(example_emotion, example_word_pairs)
    print(output)
