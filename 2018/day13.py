
import time
from curses import wrapper
import copy
from operator import itemgetter, attrgetter
import sys


cart_replacement = {
    '<': '-',
    '>': '-',
    '^': '|',
    'v': '|'
}

turns = {
    ('\\', '^'): ('<', (-1, 0)),
    ('\\', '>'): ('v', (0, 1)),
    ('\\', 'v'): ('>', (1, 0)),
    ('\\', '<'): ('^', (0, -1)),
    ('/', '^'): ('>', (1, 0)),
    ('/', '>'): ('^', (0, -1)),
    ('/', 'v'): ('<', (-1, 0)),
    ('/', '<'): ('v', (0, 1)),
}
crossings = {
    0: {
        '^': ('<', (-1, 0)),
        '>': ('^', (0, -1)),
        'v': ('>', (1, 0)),
        '<': ('v', (0, 1))
    },
    1: {
        '^': ('^', (0, -1)),
        '>': ('>', (1, 0)),
        'v': ('v', (0, 1)),
        '<': ('<', (-1, 0))
    },
    2: {
        '^': ('>', (1, 0)),
        '>': ('v', (0, 1)),
        'v': ('<', (-1, 0)),
        '<': ('^', (0, -1))
    }
}
straight_moves = {
    '^': (0, -1),
    '>': (1, 0),
    'v': (0, 1),
    '<': (-1, 0)
}


class Tracks(object):
    def __init__(self, tracks_matrix):
        self.matrix = tracks_matrix

    def get(self, position):
        return self.matrix[position[1]][position[0]]

    def is_turn(self, position):
        return self.get(position) in ['\\', '/']

    def is_crossing(self, position):
        return self.get(position) == '+'

    def draw(self, carts, screen=None):
        drawing_track = copy.deepcopy(self.matrix)
        for cart in carts:
            drawing_track[cart.y][cart.x] = 'X' if cart.crashing else cart.direction

        if screen:
            for idx, row in enumerate(drawing_track):
                screen.addstr(idx, 0, ''.join(row))
        else:
            print '\n'.join(''.join(row) for row in drawing_track)


class Cart(object):
    def __init__(self, position, direction):
        self.position = position
        self.direction = direction
        self.crossings_crossed = 0
        self.crashing = False

    @property
    def x(self):
        return self.position[0]

    @property
    def y(self):
        return self.position[1]

    def step(self, tracks, all_carts):
        if tracks.is_turn(self.position):
            new_direction, position_change = turns[(tracks.get(self.position), self.direction)]
        elif tracks.is_crossing(self.position):
            new_direction, position_change = crossings[self.crossings_crossed][self.direction]
            self.crossings_crossed = (self.crossings_crossed + 1) % 3
        else:
            position_change = straight_moves[self.direction]
            new_direction = self.direction

        self.direction = new_direction
        self.position = (self.x + position_change[0], self.y + position_change[1])

        for cart in all_carts:
            if cart is self:
                continue
            if cart.position == self.position:
                self.crashing = True
                cart.crashing = True


def main(stdscr, input_filename):
    with open(input_filename) as stream:
        carts = []
        track_dict = {
            (x, y): character
            for y, line in enumerate(stream)
            for x, character in enumerate(line.rstrip())
            if character != ' '
        }

    track_width = max(track_dict.keys(), key=itemgetter(0))[0]
    track_height = max(track_dict.keys(), key=itemgetter(1))[1]
    tracks = [
        [' '] * (track_width + 1)
        for _ in range(track_height + 1)
    ]
    for coord, value in track_dict.iteritems():
        if value in ['<', '>', '^', 'v']:
            carts.append(Cart(coord, value))
            tracks[coord[1]][coord[0]] = cart_replacement[value]
        else:
            tracks[coord[1]][coord[0]] = value

    track = Tracks(tracks)
    if stdscr:
        drawing_loop(stdscr, track, carts)
    else:
        console_loop(track, carts)

    print 'Part 2:', None


def drawing_loop(stdscr, track, carts):
    stdscr.clear()
    track.draw(carts, screen=stdscr)
    stdscr.refresh()
    any_crash = False
    while True:
        stdscr.clear()
        for cart in sorted(carts, key=attrgetter('x', 'y')):
            cart.step(track, carts)

        track.draw(carts, screen=stdscr)
        if any(cart.crashing for cart in carts):
            if not any_crash:
                any_crash = True
                crashing_cart = next(cart for cart in carts if cart.crashing)
                stdscr.addstr(len(track.matrix), 0, 'Part 1: {}'.format(crashing_cart.position))

            carts = [cart for cart in carts if not cart.crashing]

            if len(carts) == 1:
                stdscr.addstr(len(track.matrix), 0, 'Part 2: {}'.format(carts[0].position))
                stdscr.refresh()
                time.sleep(5)
                break

        stdscr.refresh()
        time.sleep(1)


def console_loop(track, carts):
    any_crash = False
    while True:
        for cart in sorted(carts, key=attrgetter('x', 'y')):
            cart.step(track, carts)

        if any(cart.crashing for cart in carts):
            if not any_crash:
                any_crash = True
                crashing_cart = next(cart for cart in carts if cart.crashing)
                print 'Part 1: {}'.format(crashing_cart.position)

            carts = [cart for cart in carts if not cart.crashing]

        if len(carts) == 1:
            print 'Part 2: {}'.format(carts[0].position)
            break


if __name__ == '__main__':
    if len(sys.argv) == 3 and sys.argv[2] == 'no_output':
        main(None, sys.argv[1])
    else:
        wrapper(main, sys.argv[1])
