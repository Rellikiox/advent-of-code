
from operator import itemgetter
import sys
import re

line_re = r'(\w+) would (gain|lose) (\d+) happiness units by sitting next to (\w+)\.'


def main(input_file):
    with open(input_file) as stream:
        happiness_dict = {}
        for line in stream:
            person_a, gain_lose, amount, person_b = re.match(line_re, line).groups()
            parsed_amount = int(amount) if gain_lose == 'gain' else -int(amount)
            current_pair_value = (
                happiness_dict.setdefault(person_a, {}).setdefault(person_b, 0) or
                happiness_dict.setdefault(person_b, {}).setdefault(person_a, 0)
            )
            happiness_dict[person_a][person_b] = current_pair_value + parsed_amount
            happiness_dict[person_b][person_a] = current_pair_value + parsed_amount

    participants = happiness_dict.keys()
    table = [''] * len(participants)
    print get_best_table(table, 0, happiness_dict)


def get_best_table(table, index, happiness_dict):
    available_guests = [key for key in happiness_dict.keys() if key not in table]
    if not available_guests:
        return table, table_value(table, happiness_dict)

    best_table = ([], None)
    current_table = list(table)
    for guest in available_guests:
        current_table[index] = guest
        best_table = max(
            [best_table, get_best_table(current_table, index + 1, happiness_dict)],
            key=itemgetter(1)
        )

    return best_table


def table_value(table, happiness_dict):
    extended_table = table + [table[0]]
    return sum(
        happiness_dict[extended_table[guest_idx]][extended_table[guest_idx + 1]]
        for guest_idx in range(len(extended_table) - 1)
    )


if __name__ == '__main__':
    main(sys.argv[1])
