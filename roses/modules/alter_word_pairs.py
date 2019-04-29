from typing import List, Tuple
import nltk
import gensim
import os
from gensim.models import FastText
from utils import read_json_file

nltk.download('abc')
nltk.download('brown')

from nltk.corpus import abc
from nltk.corpus import brown


#TODO 
# - evaluate similar words and pick a good replacement
# - make sure the return method returns the correct things
# - possibly make a way to save the model and reload it 


# we could possibly save the model to speed up the process
def train_model():

    data = read_json_file("data/bible_kjv_wrangled.json")
    sentences = list(data.values())
    
    print("-----------Tokenize corpus-------------")
    tokenized_sentences = []
    for s in sentences:
        tokens = nltk.word_tokenize(s)
        tokenized_sentences.append(tokens)

    for s in abc.sents():
        tokenized_sentences.append(s)
    
    for s in brown.sents():
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

    model = train_model()

    final_pairs = []
    for pair in word_pairs:

        changed_pair =[]
        for word in pair['word_pair']:

            similar_words_fast = model.wv.similar_by_word(word, 5)
            print("similar words to " + word , similar_words_fast)
            
            changed_pair.append(similar_words_fast[4])

        final_pairs.append(changed_pair)

    for p in final_pairs:
        print(p[0])
        print(p[1])
        print(type(p[0]))
        print("__________________")
    
    # return method needs work such that it returns the correct thing
    return [{'word_pair': (word_pair[0], word_pair[1]), 'verb': 'is'} for word_pair in final_pairs]


# For testing
if __name__ == '__main__':
    example_emotion = 'sad'
    example_word_pairs = [{'word_pair': ("human", "brutal"), 'verb': 'was'}, ]
    output = generate_word_pairs(example_emotion, example_word_pairs)
    print(output)