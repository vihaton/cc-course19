import os
import json


# TODO make this thing awesome


def read_json_file(filename):
    """
    File name regarding to roses folder.
    """
    path = get_path(filename)
    with open(path) as f:
        content = json.loads(f.read())
    return content


def get_path(filename):
    base_path = os.path.dirname(os.path.abspath(__file__))
    return "".join([base_path, "/", filename])


def get_hamming_distance(word1, word2):
    """
    Modified hamming distance. Pads words to calculate for different length words.
    :param word1:
    :param word2:
    :return:
    """
    if len(word1) >= len(word2):
        longer = word1
        shorter = word2
    else:
        longer = word2
        shorter = word1

    padded1 = f'{shorter:0>{len(longer)}}'
    padded2 = f'{shorter:0<{len(longer)}}'
    score1 = sum(c1 != c2 for c1, c2 in zip(padded1, longer))
    score2 = sum(c1 != c2 for c1, c2 in zip(padded2, longer))
    return min(score1, score2)


def get_syllables_func(syllable_dictionary):
    def get_syllables(word):
        if word in syllable_dictionary:
            return len(syllable_dictionary[word][0])
        else:
            return len(word) / 2

    return get_syllables
