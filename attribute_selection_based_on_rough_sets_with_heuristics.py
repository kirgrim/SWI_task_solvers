# Finding reducts
# Reduct is the least number of elements which preserves its indiscernible (indistinguishable) relationships
from utils import generate_sequences_from_string, sorted_string

test_table = [
    ['A1', 'B2', 'C0', 'D2', 'E0'],
    ['A2', 'B1', 'C1', 'D2', 'E2'],
    ['A2', 'B1', 'C2', 'D2', 'E2'],
    ['A1', 'B0', 'C2', 'D1', 'E1'],
    ['A1', 'B2', 'C1', 'D1', 'E1'],
    ['A2', 'B0', 'C1', 'D2', 'E2'],
    ['A2', 'B2', 'C2', 'D2', 'E0'],
    ['A1', 'B1', 'C0', 'D1', 'E1']
]

test_column_names = ['A', 'B', 'C', 'D', 'E']


def exclude_column_idxs_from_table(table, col_idxs):
    return [[item for idx, item in enumerate(column) if idx not in col_idxs] for column in table]


def scan_for_core_columns(table):
    columns_that_are_part_of_core = []
    for column_idx in range(len(test_table[0]) - 1):
        reformatted_table = exclude_column_idxs_from_table(table, col_idxs=[column_idx])
        caught_indistinguishable = {}
        for row in reformatted_table:
            attributes_combination = ''.join(row[:-1])
            if attributes_combination in caught_indistinguishable \
                    and row[-1] != caught_indistinguishable[attributes_combination]:
                columns_that_are_part_of_core.append(column_idx)
                break
            else:
                caught_indistinguishable[attributes_combination] = row[-1]
    return columns_that_are_part_of_core


def detect_rules_in_table(table):
    rule_vs_support = {}
    excluded_combinations = []
    for row in table:
        attributes_combination = ''.join(row[:-1])
        if attributes_combination not in excluded_combinations:
            if attributes_combination in rule_vs_support and row[-1] != rule_vs_support[attributes_combination]['decision_value']:
                excluded_combinations.append(attributes_combination)
            else:
                rule_vs_support.setdefault(attributes_combination, {'support': 0, 'decision_value': row[-1]})
                rule_vs_support[attributes_combination]['support'] += 1
    rule_vs_support = {k: v for k, v in rule_vs_support.items() if k not in excluded_combinations}
    return rule_vs_support


def get_letter_at_index(table, idx):
    return table[0][idx][0]


def generate_seq_of_letters(table, idxs):
    return ''.join([get_letter_at_index(table, int(idx)) for idx in idxs])


def solution(table: list = None):
    if not table:
        table = test_table
    columns_that_are_part_of_core = scan_for_core_columns(table)
    print(f'columns_that_are_part_of_core={[get_letter_at_index(table, column_that_are_part_of_core) for column_that_are_part_of_core in columns_that_are_part_of_core]}')
    processed_attribute_combinations = []
    rule_vs_support = {}
    for column_idx in columns_that_are_part_of_core:
        leftover_column_idxs = [idx for idx in range(len(table[0]) - 1) if idx != column_idx]
        possible_combinations = [str(column_idx)]
        for i in range(1, len(leftover_column_idxs)):
            possible_combinations.extend(generate_sequences_from_string(''.join([str(i) for i in leftover_column_idxs]),
                                                                        length=i))
        for combination in possible_combinations:
            parsed_indexes = set([int(s) for s in combination] + [column_idx])
            reformatted_table = exclude_column_idxs_from_table(table, [idx for idx in range(len(table[0]) - 1)
                                                                       if idx not in parsed_indexes])
            combination = "".join([table[0][idx][0] for idx in parsed_indexes])
            processed_attribute_combinations.append(combination)
            rules_in_table = detect_rules_in_table(reformatted_table)
            pretty_print_rules_in_table(combination, rules_in_table)
            rule_vs_support.update(rules_in_table)


def pretty_print_rules_in_table(combination, rules_in_table):
    print(f'Processing combination: {combination}')
    for k,v in rules_in_table.items():
        print(f'{k} -> {v["decision_value"]} s{v["support"]} c 100%')


if __name__ == '__main__':
    solution()
