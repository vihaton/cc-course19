from typing import List, Tuple
import nltk
from nltk.corpus import abc
from nltk.corpus import brown
import os
from gensim.models import FastText, KeyedVectors
import gensim.downloader as api
from random import randint

from roses.utils import read_json_file, get_path

nltk.download('abc')
nltk.download('brown')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

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


def find_alternative(word, word_vec):
    tries = 20
    while True:
        similarword = word_vec.most_similar(positive=[word[0], word[1]], topn=tries)
        tagged = nltk.pos_tag([x[0] for x in similarword])
        nouns = [x[0] for x in tagged if x[1] in ['NN', 'NNS', 'NNP', 'NNPS']]
        adjc = [x[0] for x in tagged if x[1] in ['JJ', 'JJR', 'JJS']]
        if nouns:
            if adjc:
                idx_noun = randint(0, len(nouns) - 1)
                idx_adjc = randint(0, len(adjc) - 1)
                selectend_nn = nouns[idx_noun]
                selected_jj = adjc[idx_adjc]
                return selectend_nn, selected_jj
        tries += 5


def generate_word_pairs(emotion: str, word_pairs: List[Tuple[str, str]]):
    """
    Generates a bunch of word pairs depending on input word pairs.
    """
    model_name = 'bible_model'
    model_dir = get_path('data/' + model_name)

    exists = os.path.isfile(model_dir)
    if exists:
        print('FastText Bible model already trained')
        model = FastText.load(model_dir)
    else:
        model = train_model()
        model.save(model_dir)

    wv_model_name = 'wv_model'
    wv_model_dir = get_path('data/' + wv_model_name)

    exists = os.path.isfile(wv_model_dir)
    if exists:
        print('Found a pretrained word vector model')
        word_vec = KeyedVectors.load(wv_model_dir)
    else:
        print("Loading pretrained model into memory (will take a minute)")
        word_vec = api.load("glove-wiki-gigaword-100")
        word_vec.save(wv_model_dir)
        print("LOADED AND SAVED")

    final_pairs = []

    for pair in word_pairs:
        if pair[0] in model.wv.vocab.keys() and pair[1] in model.wv.vocab.keys():
            noun, adjc = find_alternative(pair, word_vec)
            changed_pair = [noun, adjc]
            final_pairs.append(changed_pair)
        else:
            final_pairs.append([pair[0], pair[1]])

    # return method needs work such that it returns the correct thing - DONE
    return [{'word_pair': (word_pair[0], word_pair[1]), 'verb': 'is'} for word_pair in final_pairs]


# For testing
if __name__ == '__main__':
    example_emotion = 'sad'
    example_word_pairs = [("human", "brutal")]
    output = generate_word_pairs(example_emotion, example_word_pairs)
    print(output)
