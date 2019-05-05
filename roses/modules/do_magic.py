from typing import Dict, List
import nltk
import gensim
import os
from gensim.models import FastText
from random import randint

# This was a workaround for utils-module not found -error, 
# there must be a better way to do it.
import sys
sys.path.append("..") 

from roses.utils import read_json_file

# nltk.download('abc')
# nltk.download('brown')
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')

from nltk.corpus import abc
from nltk.corpus import brown

DEBUG = False


def alter_rest(emotion: str, rhyming_partials: List[Dict]):
    """
    Alters the third and fourth lines to be more creative.
    """
    if DEBUG: print(f'im alive bitches')
    model_name = 'bible_model'
    model_dir = 'roses/data/' + model_name

    exists = os.path.isfile(model_dir)
    if exists:
        print('Found a pretrained FastText model')
        model = FastText.load(model_dir)
    else:
        print("No model found")
        return rhyming_partials

    similar_to_emotion = model.wv.similar_by_word(emotion, 100)
    similar_to_emotion = [x[0] for x in similar_to_emotion]
    similar_to_emotion = nltk.pos_tag(similar_to_emotion)

    ret = []
    for partial in rhyming_partials:
        third = partial['rest'][0]
        fourth = partial['rest'][1]
        
        third = nltk.tokenize.word_tokenize(third)
        third = nltk.pos_tag(third)
        
        for x, word in enumerate(third):
            max_similarity = 0
            new_word = word
            if word[1] in ['JJ', 'JJR', 'JJS', 'NN', 'NNS', 'NNP']:
                for s in similar_to_emotion:
                    if s[1] == word[1]:
                        similarity = model.wv.similarity(s[0], word[0])
                        if similarity > max_similarity:
                            max_similarity = similarity
                            new_word = s  
                if DEBUG: print(word, "is replaced by", new_word, 'max similarity was', max_similarity)
                third[x] = new_word
        third = [x[0] for x in third]

        # TODO line 4
        fourth = nltk.tokenize.word_tokenize(fourth)
        last_word = fourth.pop(-1)
        fourth = nltk.pos_tag(fourth)

        for x, word in enumerate(fourth):
            max_similarity = 0
            new_word = word
            if word[1] in ['JJ', 'JJR', 'JJS', 'NN', 'NNS', 'NNP']:
                for s in similar_to_emotion:
                    if s[1] == word[1]:
                        similarity = model.wv.similarity(s[0], word[0])
                        if similarity > max_similarity:
                            max_similarity = similarity
                            new_word = s  
                if DEBUG: print(word, "is replaced by", new_word, 'max similarity was', max_similarity)
                fourth[x] = new_word

        fourth = [x[0] for x in fourth]
        fourth.append(last_word)
        if DEBUG: print(fourth)
        partial['rest'] = (" ".join(third), " ".join(fourth))

        ret.append(partial)

    return ret


def old_alter_rest(emotion: str, rhyming_partials: List[Dict]):
    """
    Alters the third and fourth lines to be more creative.
    """
    ret = []
    for partial in rhyming_partials:
        third = partial['rest'][0]
        fourth = partial['rest'][1]
        ret.append(partial)

    return ret


# For testing
if __name__ == '__main__':
    example_emotion = 'angry'
    example_rhyming_partials = [{'rest': ["there came an old man from his work out of the field at even", "he shall suffer loss"]}, ]
    output = alter_rest(example_emotion, example_rhyming_partials)
    print(output)