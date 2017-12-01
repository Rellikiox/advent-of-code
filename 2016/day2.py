

test_input = """
UL
UU
UR
RU
RR
RD
DR
DD
DL
LD
LL
LU
UD
"""

test_output = [1, 2, 3, 3, 6, 9, 9, 8, 7, 7, 4, 1, 5]


keypad = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]
reverse_keypad = {
    1: (0, 0),
    2: (1, 0),
    3: (2, 0),
    4: (0, 1),
    5: (1, 1),
    6: (2, 1),
    7: (0, 2),
    8: (1, 2),
    9: (2, 2),
}

actions = {
    'U': (lambda x, y: (x, max(y - 1, 0))),
    'R': (lambda x, y: (min(x + 1, 4), y)),
    'D': (lambda x, y: (x, min(y + 1, 4))),
    'L': (lambda x, y: (max(x - 1, 0), y))
}

complex_keypad = [
    [None, None, 1, None, None],
    [None, 2, 3, 4, None],
    [5, 6, 7, 8, 9],
    [None, 'A', 'B', 'C', None],
    [None, None, 'D', None, None]
]

complex_reverse_keypad = {
    1: (2, 0),
    2: (1, 1),
    3: (2, 1),
    4: (3, 1),
    5: (0, 2),
    6: (1, 2),
    7: (2, 2),
    8: (3, 2),
    9: (4, 2),
    'A': (1, 3),
    'B': (2, 3),
    'C': (3, 3),
    'D': (2, 4),
}


def get_code(input):
    output = []
    last_position = complex_reverse_keypad[5]
    for line in input.split('\n'):
        line = line.strip()
        if not line:
            continue
        number = get_number(line, last_position)
        last_position = complex_reverse_keypad[number]
        output.append(number)

    return ''.join(str(s) for s in output)


def get_number(steps, start_point):
    x, y = start_point

    for step in steps:
        new_x, new_y = actions[step](x, y)
        if complex_keypad[new_y][new_x] is not None:
            x, y = new_x, new_y

    return complex_keypad[y][x]


def main():
    for line in test_input.split('\n'):
        print line.strip(), get_number(line.strip())

    assert get_code(test_input) == test_output


if __name__ == '__main__':
    main()
