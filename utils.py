import itertools


def sorted_string(s: str):
    return ''.join(sorted(s))


def generate_sequences_from_string(lst: str, length: int):
    return set(sorted_string(''.join(set(seq)))
            for seq
            in list(itertools.combinations([x for x in lst],
                                           length)))
