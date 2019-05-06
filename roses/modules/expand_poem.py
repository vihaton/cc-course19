from typing import Dict, List

from roses.modules.to_be_or_not_to_be import fit_verb

DEBUG = False


def fill_and_create_text(emotion: str, rhyming_partials: List[Dict]):
    """
    Finishes the poem to be a 4 long list containing the poems lines.
    """
    if DEBUG:
        print(rhyming_partials[0]['rest'])
    return [
        [
            'Roses are red',
            f'{rp["word_pair"][0].capitalize()} {fit_verb(rp["word_pair"], rp["verb"])} {rp["word_pair"][1]}',
            rp['rest'][0].capitalize(),
            rp['rest'][1].capitalize()
        ]
        for rp in rhyming_partials
    ]
