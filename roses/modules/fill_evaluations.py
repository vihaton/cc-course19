from typing import List, Tuple
import numpy as np

import os
from gensim.models import FastText

from nltk.corpus import abc
from nltk.corpus import brown

from roses.utils import get_hamming_distance

DEBUG = False

# MUST TO DO
# TODO set weights for different sub evaluations to decide what we value!

# FURTHER DEVELOPMENT
# TODO evaluate novelty w.r.t. all the poems written previously (pushes the algo to search different parts of T)

def eval_semantics(poem: List[str]):
  """Does it make sense?
  
  We have no idea.
  """

  return 1


def eval_length(poem: List[str]):
    """
    Is it nice length? Penalizes long poems.

    optimal length - length.
    """
    optimal_length = 77  # scientifically proven

    length = sum(len(line) for line in poem)

    score = 150 - np.abs(optimal_length - length) # max 150
    score /= 150
    if DEBUG: print(f'\teval length score {score}')
    return score


def eval_rhytm(poem: List[str]):
    """Does it have a nice rhythm, ie. a good amount of syllables in right places?
  
  This could be done with nltk.
  """
    return 1


def eval_rhyming(poem: List[str]):
    """
    Calculating the Hamming distance of  rhyming words, to see how much the 
    words differ from each other.

    Getting first scores between 0-5, scaled to be in range 0-1. 
    If words are the same, score is zero. 
    """

    rhyme1 = poem[1].split(' ')[-1]
    rhyme2 = poem[3].split(' ')[-1]

    score = get_hamming_distance(rhyme2, rhyme1)

    scaled_score = min(score, 5)/5
    if DEBUG: print(f'\teval rhyming score {scaled_score}')
    return scaled_score


def eval_similarity_to_emotion(poem: List[str], emotion: str, model):
  """Is the feeling of the poem similar to the emotion given as input?
  
  This one could use Vord2Vec to calculate semantic distances.
  """

  if model is None:
    return 1

  score = 0
  for line in poem:
    s = model.wv.similarity(emotion, line)
    # if DEBUG: 
    #   print(f'\tsimilarity to emotion {emotion} for line \n\t\t{line} \n\t\twas {s}')
    score += s
  
  score /= 4
  if DEBUG: 
    print(f'\tsimilarity to emotion {emotion} was {score}')

  return score


def eval_dissimilarity_to_word_pairs(poem: List[str], word_pairs: List[Tuple[str, str]]):
    """Has the system been able to alter the word pair from the original input in a craetive manner?
  
  Measure distance to the original words, the longer the better. Does this make sense? IDK."""

    for pair in word_pairs:
      score = 0
      score += poem[1].find(pair[0])
      # if DEBUG: print(f'\t{poem[1]} \t{pair[0]}\n\tscore dissimilarity find {score}')
      score += poem[1].find(pair[1])
    score = np.exp(-score)
    score /= 10
    if DEBUG:
        print(f'\tscore for dissimilarity to word pairs {score}')
    return score


def evaluate_poems(emotion: str, word_pairs: List[Tuple[str, str]], poems: List[List[str]]):
  """
  Evaluates given poems and gives them a score.
  """
  model = get_fastext_model()

  scores = [0] * len(poems)
  for i, poem in enumerate(poems):
      if DEBUG:
          print(f'for poem {poem}')
      scores[i] += eval_semantics(poem)
      scores[i] += eval_length(poem)
      scores[i] += eval_rhytm(poem)
      scores[i] += eval_rhyming(poem)
      scores[i] += eval_similarity_to_emotion(poem, emotion, model)
      scores[i] += eval_dissimilarity_to_word_pairs(poem, word_pairs)

  return list(zip(poems, scores))

def get_fastext_model():
    if DEBUG: print(f'Lets fetch the model')
    model_name = 'bible_model'
    model_dir = 'roses/data/' + model_name # for production
    # if DEBUG: model_dir = '../data/' + model_name # for testing

    exists = os.path.isfile(model_dir)
    if exists:
        print('Found a pretrained FastText model for evaluation')
        return FastText.load(model_dir)
    else:
        print("No model found in ", model_dir)
        return None

def sort_poems_by_score(val):
  return -val[1]

# For testing
if __name__ == '__main__':
    example_emotion = 'sad'
    example_word_pairs = [("people", "boss"), ("animal", "legged"), ('activity', 'meeting'), 
      ('animal', 'venomous'), ('animal', 'social'), ('animal', 'unusual'), ('location', 'cemetery'), 
      ('weather', 'typhoon'), ('human', 'ruthless'), ('human', 'brutal'), ('human', 'caring'), 
      ('human', 'liberal'), ('human', 'creative'), ('human', 'barbaric')
      ]
    example_poems = [
        ["Roses are red",
         "human is boss",
         "this project is not done",
         "and you should be closs"
         ],
         ['Roses are red',
          'humane is anecdotal',
          'and see',
          'nor by battle'
         ],
         ["Roses are red",
         "human is boss",
         "this project is not done",
         "and you should be boss"
         ],
        ["Roses are red",
         "animal is legged",
         "this project is not done",
         "and you should be egged"
         ],
         ['Roses are red',
          'humanity is harmless',
          'And the sandman went killpath',
          'For a johnnie must be blameless'
         ],
         ['Roses are red',
          'humanity is happy',
          'And the sandman went dancing',
          'For a johnnie must be crappy'
         ],
         ['Roses are red',
          'humane is judicial',
          'And he set the mephibosheth which he had pilled before the comforteth in the comforteth in the sap draught when the comforteth came to drink',
          'and put it under a bushel'
         ]

    ]
    DEBUG = True
    output = evaluate_poems(example_emotion, example_word_pairs, example_poems)
    output.sort(key = sort_poems_by_score, )
    for poem in output:
      print(poem[1], poem[0])
