from typing import List, Tuple
import numpy as np

DEBUG = False


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

    score = optimal_length - length
    # score = np.sqrt(np.abs(length - optimal_length))
    # score = np.exp(-score)
    if DEBUG: print(f'\teval length score {score}')
    return score


def eval_rhytm(poem: List[str]):
    """Does it have a nice rhythm, ie. a good amount of syllables in right places?
  
  This could be done with nltk.
  """
    return 1


def eval_similarity_to_emotion(poem: List[str], emotion: str):
    """Is the feeling of the poem similar to the emotion given as input?
  
  This one could use Vord2Vec to calculate semantic distances.
  """
    return 1


def eval_dissimilarity_to_word_pairs(poem: List[str], word_pairs: List[Tuple[str, str]]):
    """Has the system been able to alter the word pair from the original input in a craetive manner?
  
  Measure distance to the original words, the longer the better. Does this make sense? IDK."""

    for pair in word_pairs:
      score = 0
      score += poem[1].find(pair[0])
      # if DEBUG: print(f'\t{poem[1]} \t{pair[0]}\n\tscore dissimilarity find {score}')
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
