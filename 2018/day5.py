
import re
import string
import sys


def main(input_file):
    with open(input_file) as stream:
        polymer = stream.read().strip()

    print 'Part 1:', len(reduce_iteratively(polymer))
    print 'Part 2:', len(reduce_with_removal(polymer))


def reduce_with_removal(polymer):
    elements = set(polymer.lower())

    return min(
        [
            reduce_via_linked_list(polymer.replace(element, '').replace(element.upper(), ''))
            for element in elements
        ],
        key=len
    )


class Node:
    def __init__(self, value, prev_node=None, next_node=None):
        self.value = value
        self.prev_node = prev_node
        self.next_node = next_node


def reduce_via_linked_list(polymer):
    # Link the list backwards
    head_node = None
    for letter in reversed(polymer):
        head_node = Node(letter, next_node=head_node)

    # And forwards
    current_node = head_node
    prev_node = None
    while current_node.next_node:
        current_node.prev_node, prev_node = prev_node, current_node

    current_node = head_node
    while current_node.next_node:
        if are_elements_reactive(current_node.value, current_node.next_node.value):
            if current_node.prev_node:
                current_node.prev_node.next_node, current_node = (
                    current_node.next_node.next_node,
                    current_node.prev_node
                )
            else:
                current_node = current_node.next_node.next_node
                head_node = current_node
        else:
            current_node = current_node.next_node


def reduce_iteratively(polymer):
    """Runs in one pass, takes ~100ms"""
    polymer = list(polymer)
    idx = 0
    while idx < len(polymer) - 1:
        element_a, element_b = polymer[idx:idx + 2]
        if are_elements_reactive(element_a, element_b):
            del polymer[idx:idx + 2]
            idx = max(idx - 1, 0)
        else:
            idx += 1
    return ''.join(polymer)


def are_elements_reactive(element_a, element_b):
    return element_a.swapcase == element_b


def reduce_by_regexp(polymer):
    """Runs in n passes, takes ~20s"""
    regex = build_regexp()
    while regex.search(polymer):
        polymer = re.sub(regex.pattern, '', polymer)
    return polymer


def build_regexp():
    regex_parts = [
        '({lower}{upper})|({upper}{lower})'.format(lower=lower, upper=upper)
        for lower, upper in zip(string.lowercase, string.uppercase)
    ]
    return re.compile(r'{}'.format('|'.join(regex_parts)))


if __name__ == '__main__':
    main(sys.argv[1])
