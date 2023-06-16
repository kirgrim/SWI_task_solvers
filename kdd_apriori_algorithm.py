# KDD Apriori Algorithm
import copy
import itertools

from utils import sorted_string, generate_sequences_from_string

test_transactions = [
    'ACDFG',
    'ABCDF',
    'CDE',
    'ADF',
    'ACDEF',
    'BCDEFG'
]

test_min_support = 3

test_confidence = 0.75


def get_confidence_value_based_on_state(source_value: int, included_elements: list = None,):
    # edge-case: 1 element set
    if not included_elements:
        return source_value


def sequence_not_contains_excluded_elements(sequence: str, excluded_elements: list):
    return all(sorted_string(excluded_element) not in sorted_string(sequence) for excluded_element in excluded_elements)


def is_subset_of(subset, superset):
    return all(item in superset and subset.count(item) == superset.count(item) for item in subset)


def strike(text):
    return ''.join([u'\u0336{}'.format(c) for c in text])


def sort_dict_keys_by_length(d: dict):
    return sorted(list(d), reverse=True, key=lambda x: len(x))


def compose_representative_sets(d: dict) -> dict:
    # we remove all the subset keys, we need only max cardinality
    d_copy = copy.copy(d)
    for superset_key in sorted(list(d), reverse=True, key=lambda x: len(x)):
        d = {k: v for k, v in d.items() if not is_subset_of(k, superset_key)
             or k == superset_key or v > d_copy[superset_key] and len(k) > 1}
    return d


def compose_representative_rules(representative_sets, included_elements_vs_confidence, min_confidence):
    representative_rules = {}
    for set_key in sort_dict_keys_by_length(representative_sets):
        used_letters = []
        print(f'Representative Rules for {set_key}')
        for _len in range(1, len(set_key)):
            all_combinations = generate_sequences_from_string(set_key, _len)
            for combination in [combination for combination in all_combinations
                                if not any(letter in combination for letter in used_letters)]:
                letters_in_combination = [letter for letter in combination]
                implication = ''.join([x for x in set_key if x not in letters_in_combination])
                confidence = round(representative_sets[set_key] / included_elements_vs_confidence[combination], 2)
                draw_str = f'{combination} -> {implication} {confidence} {min_confidence*100}%'
                if confidence >= min_confidence:
                    used_letters.extend(letters_in_combination)
                    representative_rules[f"{combination} -> {implication}"] = confidence
                    print(draw_str)
                else:
                    print(strike(draw_str))
                # print(all_combinations)
    return representative_rules


def solution(transactions: list = None, min_support: int = None, min_confidence: int = None,):
    if not transactions:
        transactions = test_transactions
    if not min_support:
        min_support = test_min_support
    if not min_confidence:
        min_confidence = test_confidence
    included_elements_vs_confidence = {}
    excluded_elements_vs_confidence = {}
    current_sequence_included_elements = 'UNDEFINED'
    current_sequence_length = 0
    while current_sequence_included_elements:
        current_sequence_length += 1
        # keys are unique elements; values are "confidence" - number of its occurance
        unique_sequences_to_confidence = dict()

        unique_sequences = set()
        if current_sequence_length == 1:
            for transaction in transactions:
                unique_sequences |= set([letter for letter in transaction])
        else:
            unique_sequences = set(sorted_string(''.join(set(seq)))
                                   for seq
                                   in list(itertools.combinations(list(included_elements_vs_confidence),
                                           current_sequence_length)))
        for transaction in transactions:
            for sequence in unique_sequences:
                if is_subset_of(sequence, transaction):
                    unique_sequences_to_confidence.setdefault(sequence, 0)
                    unique_sequences_to_confidence[sequence] += 1
        # print(f"All {unique_sequences_to_confidence=}")
        # print(f'Filtering those which has support smaller than {min_support=}')
        # Filtering results based on "min_support" threshold
        # print(f'{excluded_elements=}')
        current_sequence_included_elements = {k: v
                                              for k, v in unique_sequences_to_confidence.items()
                                              if v >= min_support
                                              and (not excluded_elements_vs_confidence
                                                   or sequence_not_contains_excluded_elements(k,
                                                                                              list(excluded_elements_vs_confidence)))}
        included_elements_vs_confidence.update(current_sequence_included_elements)
        print(f"Filtered {unique_sequences_to_confidence=}")
        excluded_elements_vs_confidence.update({k: v for k, v in unique_sequences_to_confidence.items() if v < min_support})
    print(f'{excluded_elements_vs_confidence=}')
    print(f'{included_elements_vs_confidence=}')

    representative_sets = compose_representative_sets(included_elements_vs_confidence)

    print(f'{representative_sets=}')

    print('Composing Representative Rules')
    representative_rules = compose_representative_rules(representative_sets, included_elements_vs_confidence,
                                                        min_confidence=min_confidence)
    pretty_print_representative_rules(representative_rules)


def pretty_print_representative_rules(representative_rules):
    print('Representative Rules')
    for k, v in representative_rules.items():
        print(f'{k} {v*100}%')


if __name__ == '__main__':
    solution()
