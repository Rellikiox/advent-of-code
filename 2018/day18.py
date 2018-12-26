
from operator import itemgetter
import time
import curses
import sys


def get_neighbours(coord):
    x, y = coord
    return [
        (x - 1, y - 1), (x, y - 1), (x + 1, y - 1),
        (x - 1, y), (x + 1, y),
        (x - 1, y + 1), (x, y + 1), (x + 1, y + 1),
    ]


def main(screen, input_filename, times):
    data = {}
    with open(input_filename) as stream:
        for y, row in enumerate(stream):
            for x, char in enumerate(row.strip()):
                data[(x, y)] = char

    data = dict(data)
    max_y = max(data.keys(), key=itemgetter(1))[1]
    for iteration in range(times):
        new_data = {}
        for coord, acre in data.iteritems():
            if acre == '.':
                n_trees = sum(data.get(neighbour) == '|' for neighbour in get_neighbours(coord))
                if n_trees >= 3:
                    new_data[coord] = '|'
            elif acre == '|':
                n_lumber = sum(data.get(neighbour) == '#' for neighbour in get_neighbours(coord))
                if n_lumber >= 3:
                    new_data[coord] = '#'
            else:
                neighbours = [data.get(neighbour) for neighbour in get_neighbours(coord)]
                n_trees = sum(neighbour == '|' for neighbour in neighbours)
                n_lumber = sum(neighbour == '#' for neighbour in neighbours)
                if n_trees >= 1 and n_lumber >= 1:
                    new_data[coord] = '#'
                else:
                    new_data[coord] = '.'

        data.update(new_data)
        if screen:
            screen.clear()
            time.sleep(0.1)
            for coord, acre in data.iteritems():
                screen.addch(coord[1], coord[0], acre)

            value = (
                sum(acre == '|' for acre in data.values()) *
                sum(acre == '#' for acre in data.values())
            )
            screen.addstr(max_y + 1, 0, str(value))
            screen.refresh()

        if (iteration + 1) % 100 == 0:
            value = (
                sum(acre == '|' for acre in data.values()) *
                sum(acre == '#' for acre in data.values())
            )
            print '{}: {}'.format(iteration + 1, value)

    value = (
        sum(acre == '|' for acre in data.values()) *
        sum(acre == '#' for acre in data.values())
    )

    print 'Value :', value


if __name__ == '__main__':
    if 'noscreen' in sys.argv:
        main(None, sys.argv[1], int(sys.argv[2]))
    else:
        curses.wrapper(main, sys.argv[1], int(sys.argv[2]))
