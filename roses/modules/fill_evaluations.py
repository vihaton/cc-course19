from typing import List, Tuple

import nltk
import numpy as np

from roses.utils import get_syllables_func

SCALE = (0, 1)

DEBUG = False

syllable_dictionary = nltk.corpus.cmudict.dict()


# TODO evaluate novelty w.r.t. all the poems written previously (pushes the algo to search different parts of T)


def eval_semantics(poem: List[str]):
    """
    Does it make sense?

    We have no idea.
    """

    return 1


def eval_length(poem: List[str]):
    """
    Is it nice length?
    exp(- Square root of the absolute distance to the optimal length).
    """
    optimal_length = 77  # scientifically proven

    length = sum(len(line) for line in poem)

    score = np.sqrt(np.abs(length - optimal_length))
    score = np.exp(-score)
    if DEBUG:
        print(f'\teval length score {score}')
    return score


def eval_rhytm(poem: List[str]):
    """
    Does it have a nice rhythm, ie. a good amount of syllables in right places?

    Just compares syllable amounts for 2nd and 4th line. Smaller score if it differs more.
    Should it check other lines? Something else?
    """

    penalty = 0.05
    line_syllables = [0, 0, 0, 0]
    for i, line in enumerate(poem):
        line_syllables[i] = sum(map(get_syllables_func(syllable_dictionary), line.split(' ')))

    diff_1_3 = abs(line_syllables[1] - line_syllables[3])
    value = np.clip(1 - penalty * diff_1_3, *SCALE)
    if DEBUG:
        print(f'Rythm score: {value}')
    return value


def eval_similarity_to_emotion(poem: List[str], emotion: str):
    """
    Is the feeling of the poem similar to the emotion given as input?

    This one could use Vord2Vec to calculate semantic distances.
    """
    return 1


def eval_dissimilarity_to_word_pairs(poem: List[str], word_pairs: List[Tuple[str, str]]):
    """
    Has the system been able to alter the word pair from the original input in a craetive manner?

    Measure distance to the original words, the longer the better. Does this make sense? IDK.
    """

    score = 0
    print(poem[1])
    for pair in word_pairs:
        print(pair)
        score += poem[1].find(pair[0])
        score += poem[1].find(pair[1])
    score = np.exp(-score)
    if DEBUG:
        print(f'\tscore for dissimilarity to word pairs {score}')
    return score


def evaluate_poems(emotion: str, word_pairs: List[Tuple[str, str]], poems: List[List[str]]):
    """
    Evaluates given poems and gives them a score.
    """

    scores = [0] * len(poems)
    for i, poem in enumerate(poems):
        if DEBUG:
            print(f'for poem {poem}')
        scores[i] += eval_semantics(poem)
        scores[i] += eval_length(poem)
        scores[i] += eval_rhytm(poem)
        scores[i] += eval_similarity_to_emotion(poem, emotion)
        scores[i] += eval_dissimilarity_to_word_pairs(poem, word_pairs)

    return list(zip(poems, scores))


# For testing
if __name__ == '__main__':
    example_emotion = 'sad'
    example_word_pairs = [('people', 'boss'), ('animal', 'legged')]
    example_poems = [
        ['Roses are red',
         'human is boss',
         'this project is not done',
         'and you should be closs'
         ],
        ['Roses are red',
         'animal is legged',
         'this project is not done',
         'and you should be egged'
         ],
        [
            'Roses are red',
            'inhuman is visual',
            'neither was there gentleness in them any heavier',
            'let lukewarm eyes behold the things that are equal'
        ]
    ]
    DEBUG = True
    output = evaluate_poems(example_emotion, example_word_pairs, example_poems)
    print(output)
