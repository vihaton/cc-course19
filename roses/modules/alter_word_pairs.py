from typing import List, Tuple
import nltk
import gensim
from utils import read_json_file


# we could possibly save the model to speed up the process
def train_model():
    nltk.download('abc')
    from nltk.corpus import abc

    data = read_json_file("data/bible_kjv_wrangled.json")
    sentences = list(data.values())
   
    tokenized_sentences = []
    for s in sentences:
        tokens = nltk.word_tokenize(s)
        tokenized_sentences.append(tokens)

    for s in abc.sents():
        tokenized_sentences.append(s)

    model= gensim.models.Word2Vec(tokenized_sentences)
    X= list(model.wv.vocab)

    return model, X



def generate_word_pairs(emotion: str, word_pairs: List[Tuple[str, str]]):
    """
    Generates a bunch of word pairs depending on input word pairs and emotion.
    """

    model, vocab = train_model()

    for pair in word_pairs:
        for word in pair['word_pair']:
            similar_words = model.similar_by_word(word, 8)
            print("similar words to " + word , similar_words)
            


    return [{'word_pair': (word_pair[0], word_pair[1]), 'verb': 'is'} for word_pair in word_pairs]


# For testing
if __name__ == '__main__':
    example_emotion = 'sad'
    example_word_pairs = [{'word_pair': ("human", "god"), 'verb': 'was'}, 
                            {'word_pair': ('animal', 'legged'), 'verb': 'is'}]
    DEBUG = False
    output = generate_word_pairs(example_emotion, example_word_pairs)
    print(output)