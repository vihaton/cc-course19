from typing import List, Tuple
import nltk
import gensim
import os
from gensim.models import FastText
from random import randint

# This was a workaround for utils-module not found -error, 
# there must be a better way to do it.
import sys
sys.path.append("..") 

from utils import read_json_file

nltk.download('abc')
nltk.download('brown')
nltk.download('punkt')

from nltk.corpus import abc
from nltk.corpus import brown


#TODO 
# - evaluate similar words and pick a good replacement
# - make sure the return method returns the correct things - DONE
# - possibly make a way to save the model and reload it - STARTED, runs nicely here
#       but doesn't work from main.py yet 


# we could possibly save the model to speed up the process - STARTED
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
        s = list(filter(lambda x:x.isalpha() and len(x)>1, s))
        s = [x.lower() for x in s] # Do we want everything in lowercase?
        tokenized_sentences.append(s)
    
    for s in brown.sents():
        s = list(filter(lambda x:x.isalpha() and len(x)>1, s))
        s = [x.lower() for x in s] # Do we want everything in lowercase?
        tokenized_sentences.append(s)

    print("------------TRAINING FASTTEXT-----------")
    
    model = FastText(tokenized_sentences, size=100, window=5, min_count=5, workers=4,sg=1)

    print("----------------DONE-------------")
    return model

def evaluate_replacement():
    return 0
    
def generate_word_pairs(emotion: str, word_pairs: List[Tuple[str, str]]):
    """
    Generates a bunch of word pairs depending on input word pairs and emotion.
    """

    model_name = 'bible_model'
    model_dir = '../data/' + model_name

    exists = os.path.isfile(model_dir)
    if exists:
        print('Found a pretrained FastText model')
        model = FastText.load(model_dir)
    else:
        model = train_model()
        model.save(model_dir)
    print(model)

    final_pairs = []
    for pair in word_pairs:

        #changed_pair =[]
        noun = find_alternative(pair['word_pair'][0], ['NN', 'NNS', 'NNP', 'NNPS'], model)
        adjective = find_alternative(pair['word_pair'][1], ['JJ', 'JJR', 'JJS'], model)
        changed_pair = [noun, adjective]

        """
        for word in pair['word_pair']:

            similar_words_fast = model.wv.similar_by_word(word, 10)
            print("similar words to " + word , similar_words_fast)
            
            changed_pair.append(similar_words_fast[4])
        """

        final_pairs.append(changed_pair)

    for p in final_pairs:
        print(p[0])
        print(p[1])
        print(type(p[0]))
        print("__________________")
    
    # return method needs work such that it returns the correct thing - DONE
    return [{'word_pair': (word_pair[0], word_pair[1]), 'verb': 'is'} for word_pair in final_pairs]

def find_alternative(word, part_of_speechs, model):
    tries = 10
    while True:
        similar_words_fast = model.wv.similar_by_word(word, tries)
        print("similar words to " + word , similar_words_fast)

        tagged = nltk.pos_tag([x[0] for x in similar_words_fast])
        right_part = [x[0] for x in tagged if x[1] in part_of_speechs]
        if right_part:
            index = randint(0, len(right_part))
            return right_part[index]
        tries += 10 
    #return 'foo'


# For testing
if __name__ == '__main__':
    example_emotion = 'sad'
    example_word_pairs = [{'word_pair': ("human", "brutal"), 'verb': 'was'}]
    output = generate_word_pairs(example_emotion, example_word_pairs)
    print(output)