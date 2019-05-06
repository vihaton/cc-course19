import random
import string
from typing import Dict, List

from roses.utils import read_json_file

DEBUG = False


def find_lines(emotion: str, rhyming_partials: List[Dict]):
    """
    Creates combinations of ending lines (3rd and 4th) from some knowledgebase.
    """

    data = read_json_file("data/bible_kjv_wrangled.json")

    keys, last_words_of_sentences = extract_keys_sentences_last_words(data)

    if DEBUG:
        print(f'\nchoose_lines,\n\tkeys length {len(keys)}'
              f'\n\n\tlength last words of sentences {len(last_words_of_sentences)}')
    ret = []
    for partial in rhyming_partials:
        for word in partial['rhymes']:
            rhyming_sentences = []
            indices = [i for i, x in enumerate(last_words_of_sentences) if x == word]
            if indices:
                for ix in indices:
                    rhyming_sentences.append(keys[ix])

            if DEBUG:
                print(f'rhyming sentences in choose lines {rhyming_sentences}')
            for generated_partial in generate_partials(data, partial, rhyming_sentences):
                ret.append(generated_partial)
    return ret


def generate_partials(corpus: Dict, partial: Dict, rhyming_keys):
    new_partials = []
    for rhyme_key in rhyming_keys:
        third = corpus[random.choice(list(corpus))]
        fourth = corpus[rhyme_key]

        new_partial = partial.copy()
        new_partial['rest'] = (third, fourth)
        new_partials.append(new_partial)
    return new_partials


def extract_keys_sentences_last_words(corpus: Dict):
    # There probably is a better/faster way to do this using dictionaries but I dont know how rn
    keys = []
    last_words_of_sentences = []

    for key, value in corpus.items():
        keys.append(key)
        last_word_of_sentence = value.translate(str.maketrans('', '', string.punctuation))
        last_word_of_sentence = last_word_of_sentence.strip().split(' ')[-1]
        last_words_of_sentences.append(last_word_of_sentence.lower())

    return keys, last_words_of_sentences


# For testing
if __name__ == '__main__':
    DEBUG = True
    example_emotion = 'sad'
    # the following is a legit input from a run, which produced 1 poem when it was asked for 5
    example_rhyming_partials = [{'word_pair': ('sensitivity', 'fleeting'), 'verb': 'is',
                                 'rhymes': ['abrogating', 'abdicating', 'abetting', 'abbreviating', 'aborting',
                                            'abducting', 'accelerating', 'abating', 'abutting']},
                                {'word_pair': ('inhumane', 'autonomous'), 'verb': 'is',
                                 'rhymes': ['artemus', 'autonomous', 'amos', 'bemis', 'brademas', 'animous',
                                            'anonymous', 'animists', 'blasphemous', 'animus']},
                                {'word_pair': ('inhumane', 'societal'), 'verb': 'is',
                                 'rhymes': ['anecdotal', 'antal', 'aristotle', 'austell', 'acquittal', 'accidental',
                                            'apostol', 'antle', 'artiodactyl']},
                                {'word_pair': ('canal', 'obnoxious'), 'verb': 'is',
                                 'rhymes': ['anxious', 'cautious', 'ambitious', 'ceraceous', 'atrocious', 'capricious',
                                            'auspicious', 'audacious', 'capacious']},
                                {'word_pair': ('provocation', 'angular'), 'verb': 'is',
                                 'rhymes': ['bacheller', 'babler', 'annular', 'bachelor', 'abler', 'aumiller',
                                            'angular', 'appenzeller', 'alveolar', 'avuncular']},
                                {'word_pair': ('winter', 'ngc'), 'verb': 'is', 'rhymes': []},
                                {'word_pair': ('hume', 'relentless'), 'verb': 'is',
                                 'rhymes': ["analyst's", "analysts'", 'allis', 'amaryllis', 'annapolis', 'alice',
                                            'alyce', 'angeles', 'alexopoulos', 'analysts']},
                                {'word_pair': ('humane', 'meningococcal'), 'verb': 'is', 'rhymes': []},
                                {'word_pair': ('hume', 'lng'), 'verb': 'is', 'rhymes': []},
                                {'word_pair': ('humanism', 'governmental'), 'verb': 'is',
                                 'rhymes': ['anecdotal', 'antal', 'aristotle', 'austell', 'acquittal', 'accidental',
                                            'apostol', 'antle', 'artiodactyl', 'anecdotal', 'antal', 'aristotle',
                                            'austell', 'acquittal', 'accidental', 'apostol', 'antle', 'artiodactyl']},
                                {'word_pair': ('inhuman', 'imaginative'), 'verb': 'is',
                                 'rhymes': ['additive', 'abortive', 'adaptive', 'active', 'acquisitive', 'addictive',
                                            'accusative', 'accommodative', 'accumulative']},
                                {'word_pair': ('hume', 'hudson'), 'verb': 'is',
                                 'rhymes': ['abelson', 'acheson', 'ackerson', 'aaronson', 'abrahamson', 'abrahamsen',
                                            'abramson', 'aasen', 'acuson']}]

    output = find_lines(example_emotion, example_rhyming_partials)
    print(output)
