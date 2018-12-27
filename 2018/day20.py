
import cProfile
from Queue import deque
import sys


MOVEMENT = {
    'N': (0, -1),
    'E': (1, 0),
    'S': (0, 1),
    'W': (-1, 0)
}


def build_map(regex):
    x, y = (0, 0)
    floor = {(x, y): 0}
    positions = deque([(x, y)])
    for char in regex[1:-1]:
        if char == '(':
            positions.appendleft((x, y))
        elif char == ')':
            x, y = positions.popleft()
        elif char == '|':
            x, y = positions[0]
        else:
            prev_dist = floor[(x, y)]
            _x, _y = MOVEMENT[char]
            x, y = (x + _x, y + _y)
            floor[(x, y)] = min(floor.get((x, y), float('inf')), prev_dist + 1)

    return floor


def main(input_filename):
    with open(input_filename) as stream:
        data = stream.read().strip()

    floor = build_map(data)

    print 'Part 1:', max(floor.values())
    print 'Part 2:', sum(value >= 1000 for value in floor.values())


if __name__ == '__main__':
    if 'debug' in sys.argv:
        cProfile.run('main(sys.argv[1])')
    else:
        main(sys.argv[1])
