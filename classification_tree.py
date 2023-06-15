from dataclasses import dataclass

import numpy as np

mylist = [1, 2, 3, 4, 5, 6]
result = np.prod(np.array(mylist))

# Constructs a Decision Tree Using the Gini Index


# attributes = ['M', 'N', 'Q']


@dataclass
class Rule:
    tree_path: list
    support: int
    confidence_percentage: int = 100


sample_tree = [
    ['m1', 'n3', 'q2', 'r2'],
    ['m2', 'n3', 'q2', 'r1'],
    ['m2', 'n2', 'q1', 'r1'],
    ['m1', 'n2', 'q1', 'r2'],
    ['m2', 'n1', 'q3', 'r2'],
    ['m1', 'n1', 'q3', 'r2'],
    ['m2', 'n3', 'q1', 'r1'],
    ['m1', 'n2', 'q2', 'r2'],
]


def get_column_at_index(matrix_2d, idx) -> list:
    return [row[idx] for row in matrix_2d]


def product(lst: list) -> float:
    prod = 1
    for x in lst:
        prod *= x

    return prod


def get_attribute_probabilities(column, verbose: bool = False) -> dict:
    attribute_probabilities = {}
    for decision_attribute in set(column):
        if verbose:
            print(f'p({decision_attribute}) = {column.count(decision_attribute)}/{len(column)}')
        attribute_probabilities[decision_attribute] = column.count(decision_attribute)/len(column)
    return attribute_probabilities


def get_key_with_max_value(_dict: dict) -> str:
    return max(_dict, key=_dict.get)


def get_all_max_value_keys(_dict: dict) -> str:
    rand_max_value_key = get_key_with_max_value(_dict)
    return [x for x in list(_dict) if _dict[rand_max_value_key] == _dict[x]]


def get_gini_value_of_decision_attributes(source_table, verbose: bool = False):
    last_column = get_column_at_index(matrix_2d=source_table, idx=-1)
    decision_attribute_probabilities = get_attribute_probabilities(last_column, verbose=verbose)
    gini = product(decision_attribute_probabilities.values())
    if verbose:
        print(f'GINI = {"*".join(list([str(x) for x in decision_attribute_probabilities.values()]))} = {gini}')
    return gini


def get_column_index_by_value(source_table, val: str) -> int:
    for i in range(len(source_table[0])):
        if source_table[0][i].startswith(val):
            return i


def get_num_lines_matching_decision_attribute(source_table, attribute_name, decision_attribute):
    attribute_col_idx = get_column_index_by_value(source_table, attribute_name[0])
    return len(list(filter(lambda line: line[attribute_col_idx] == attribute_name
                                        and line[-1] == decision_attribute,
                           source_table)))


def calculate_gini_score_for_attributes(source_table, attributes, decision_attributes_distinct):
    gini_probabilities = {}
    for i in range(len(attributes)):
        gini_probabilities[attributes[i]] = 0
        column = get_column_at_index(source_table, i)
        attribute_probabilities = get_attribute_probabilities(column)
        probs_expression = []
        for attribute_name, attribute_probability in attribute_probabilities.items():
            gini_attribute_probability = attribute_probability
            probs_product = f'{attribute_probability} * ('
            for decision_attribute in decision_attributes_distinct:
                num_pairs = get_num_lines_matching_decision_attribute(source_table, attribute_name, decision_attribute)
                if probs_product.endswith('('):
                    probs_product += f'{num_pairs} / {column.count(attribute_name)}'
                else:
                    probs_product += f' * {num_pairs} / {column.count(attribute_name)}'
                gini_attribute_probability *= num_pairs / column.count(attribute_name)
            gini_probabilities[attributes[i]] += gini_attribute_probability
            probs_product += ')'
            probs_expression.append(probs_product)
        gini_probabilities[attributes[i]] = round(gini_probabilities[attributes[i]], 6)
        gini_calculation_str = ' + '.join(probs_expression)
        print(f'Gini({attributes[i].upper()}) = {gini_calculation_str} = {gini_probabilities[attributes[i]]}')
    return gini_probabilities


def calculate_gini_gains(gini_probabilities, decision_column_gini_score):
    gini_gains = {}
    for attribute_name, attribute_gini_value in gini_probabilities.items():
        gini_gains[attribute_name] = round(decision_column_gini_score - attribute_gini_value, 6)
        print(f'GiniGain({attribute_name.upper()}) = {decision_column_gini_score} - {attribute_gini_value} = {gini_gains[attribute_name]}')
    return gini_gains


def construct_rules(source_table, max_gini_gain_col_idx, decision_attributes_distinct, from_attributes: list = None):
    if not from_attributes:
        from_attributes = []
    else:
        from_attributes = from_attributes.copy()
    max_gini_gain_col = get_column_at_index(source_table, max_gini_gain_col_idx)
    max_gini_gain_col_distinct = set(max_gini_gain_col)
    rules = []
    justified_attributes = []
    for attribute in max_gini_gain_col_distinct:
        total_number_of_items = max_gini_gain_col.count(attribute)
        for decision_attribute in decision_attributes_distinct:
            number_of_matching_decision_attributes = get_num_lines_matching_decision_attribute(source_table, attribute, decision_attribute)
            if number_of_matching_decision_attributes == total_number_of_items:
                rules.append(Rule(tree_path=from_attributes + [attribute, decision_attribute],
                                  support=number_of_matching_decision_attributes))
                justified_attributes.append(attribute)
    return rules, [attribute for attribute in max_gini_gain_col_distinct if attribute not in justified_attributes]


def shrink_source_table_to_attribute_values(source_table, attribute_filters: list):
    max_gini_gain_col_idx = get_column_index_by_value(source_table, attribute_filters[0][0])
    res_table = source_table.copy()
    # shrink by rows
    res_table = [row for row in res_table if row[max_gini_gain_col_idx] in attribute_filters]
    # eliminate redundant column
    res_table = [[x for x in row if x[0] != attribute_filters[0][0]] for row in res_table]
    return res_table


def solution(source_table: list[list] = None, tree_root_attributes: list = None):
    all_rules = []
    if not source_table:
        source_table = sample_tree
    if not tree_root_attributes:
        tree_root_attributes = []
    print('Starting Creating Decision Tree by Gini Score')
    # Decision attributes are those that are latest in tree
    gini = get_gini_value_of_decision_attributes(source_table=source_table, verbose=True)

    # Calculating gini score for attributes
    attributes = [x[0] for x in source_table[0][:-1]]
    last_column = get_column_at_index(matrix_2d=source_table, idx=-1)
    decision_attributes_distinct = set(last_column)
    gini_probabilities = calculate_gini_score_for_attributes(source_table, attributes, decision_attributes_distinct)
    gini_gains = calculate_gini_gains(gini_probabilities, decision_column_gini_score=gini)
    max_gini_gain_attributes = get_all_max_value_keys(gini_gains)
    for max_gini_gain_attribute in max_gini_gain_attributes:
        tree_root_attributes_copy = tree_root_attributes.copy()
        max_gini_gain_col_idx = get_column_index_by_value(source_table, max_gini_gain_attribute)
        rules, leftover_attributes = construct_rules(source_table, max_gini_gain_col_idx,
                                                     decision_attributes_distinct,
                                                     from_attributes=tree_root_attributes_copy)
        all_rules.extend(rules)
        if leftover_attributes:
            if len(leftover_attributes) == 1:
                tree_root_attributes_copy.append(leftover_attributes[0])
            shrunk_table = shrink_source_table_to_attribute_values(source_table, leftover_attributes)
            # tree_root_attributes_copy.append(max_gini_gain_attribute)
            all_rules.extend(solution(shrunk_table, tree_root_attributes=tree_root_attributes_copy))
    return all_rules


def pretty_print(rules: list[Rule]):
    for rule in rules:
        print(f'{" * ".join(rule.tree_path[:-1])} -> {rule.tree_path[-1]}\n'
              f'Support - {rule.support}\n'
              f'Confidence - {rule.confidence_percentage}%\n\n')


if __name__ == '__main__':
    pretty_print(solution())

