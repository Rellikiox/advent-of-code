"""
we have a 4*4 grid, there are either open or closed doors between each room

        #########
        #S| | | #
        #-#-#-#-#
        # | | | #
        #-#-#-#-#
        # | | | #
        #-#-#-#-#
        # | | |
        ####### V

starting at pos 0.0 and have a given passcode, you need to get to pos 4.4,
you can only pass through open doors

to know if a room is open you have to:
    - hash your current passcode and take the first 4 characters, which
    correspond to UP DOWN LEFT and RIGHT
        - if the char is in 'bcdef' the door is open
        - if the char is in '0123456789a' the door is closed
    - once you move to a new room you add the move you made (U, D, L, R) to the hash
"""

import hashlib
from collections import namedtuple

test_data = [
    ('ihgpwlah', 'DDRRRD'),
    ('kglvqrro', 'DDUDRLRRUDRD'),
    ('ulqzkmiv', 'DRURDRUDDLLDLUURRDULRLDUUDDDRR')
]

test_data_2 = [
    ('ihgpwlah', 370),
    ('kglvqrro', 492),
    ('ulqzkmiv', 830)
]

open_chars = 'bcdef'
new_direction = {
    'U': lambda x, y: (x, y - 1),
    'D': lambda x, y: (x, y + 1),
    'L': lambda x, y: (x - 1, y),
    'R': lambda x, y: (x + 1, y)
}
is_open = {
    'U': lambda h: h[0] in open_chars,
    'D': lambda h: h[1] in open_chars,
    'L': lambda h: h[2] in open_chars,
    'R': lambda h: h[3] in open_chars
}

Position = namedtuple('Position', ['x', 'y', 'path'])


def md5(data):
    return hashlib.md5(data).hexdigest()


def get_new_dir_if_valid(pos, direction):
    new_x, new_y = new_direction[direction](pos.x, pos.y)
    if 0 <= new_x <= 3 and 0 <= new_y <= 3 and is_open[direction](md5(pos.path)):
        return Position(new_x, new_y, pos.path + direction)


def shortest_path(initial_hash):
    frontier = [Position(0, 0, initial_hash)]
    while frontier:
        current_pos = frontier.pop(0)
        for direction in ['U', 'D', 'L', 'R']:
            new_dir = get_new_dir_if_valid(current_pos, direction)
            if new_dir:
                if new_dir.x == 3 and new_dir.y == 3:
                    return new_dir.path[len(initial_hash):]

                frontier.append(new_dir)


def longest_path(initial_hash):
    longest_path = ''
    frontier = [Position(0, 0, initial_hash)]
    while frontier:
        current_pos = frontier.pop(0)
        for direction in ['U', 'D', 'L', 'R']:
            new_dir = get_new_dir_if_valid(current_pos, direction)
            if new_dir:
                if new_dir.x == 3 and new_dir.y == 3:
                    if len(new_dir.path) > len(longest_path):
                        longest_path = new_dir.path
                else:
                    frontier.append(new_dir)

    return len(longest_path[len(initial_hash):])


def main():
    # for data in test_data:
    #     path = shortest_path(data[0])
    #     print path == data[1], path, data[1]
    for data in test_data_2:
        path = longest_path(data[0])
        print len(path) == data[1], len(path)


if __name__ == '__main__':
    main()
