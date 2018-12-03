
from itertools import groupby
import sys


def main(input_file):
    with open(input_file) as stream:
        box_ids = stream.read().split('\n')

    count_2 = 0
    count_3 = 0
    for box_id in box_ids:
        appearing_letter_counts = {
            len(list(group[1])) for group in groupby(sorted(box_id))
        }
        count_2 += 2 in appearing_letter_counts
        count_3 += 3 in appearing_letter_counts

    print 'Part 1:', count_2 * count_3

    for index_a in range(len(box_ids) - 1):
        box_a = box_ids[index_a]
        for index_b in range(index_a + 1, len(box_ids)):
            box_b = box_ids[index_b]
            if string_diff(box_a, box_b) == 1:
                print 'Part 2:', remove_diff(box_a, box_b)
                break


def string_diff(string_a, string_b):
    return sum(
        letter_a != letter_b
        for letter_a, letter_b in zip(string_a, string_b)
    )


def remove_diff(string_a, string_b):
    return ''.join(
        letter_a
        for letter_a, letter_b in zip(string_a, string_b)
        if letter_a == letter_b
    )


if __name__ == '__main__':
    main(sys.argv[1])
