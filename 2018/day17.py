
import sys
import time
from collections import namedtuple
from functools import partial
from itertools import product
from operator import attrgetter, itemgetter

import curses

Coordinate = namedtuple('Coordinate', ['x', 'y'])


def parse_value(value):
    if '..' in value:
        start, end = [int(v) for v in value[2:].split('..')]
        return range(start, end + 1)
    else:
        return [int(value[2:])]


def parse_coordinates(raw_coordinates):
    coordinates = []
    for row in raw_coordinates.strip().split('\n'):
        if row.startswith('x'):
            x, y = [parse_value(v.strip()) for v in row.split(',')]
        else:
            y, x = [parse_value(v.strip()) for v in row.split(',')]

        coordinates.append(Coordinate(x, y))
    return coordinates


def get_min_max(values, attr):
    return (
        getattr(min(values, key=attrgetter(attr)), attr),
        getattr(max(values, key=attrgetter(attr)), attr)
    )


class Drop(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.flowing = True

    @property
    def still(self):
        return not self.flowing


class Ground(object):
    def __init__(self, ground):
        self.ground = ground
        self.water = []
        self.water_tiles = {}
        self.min_x, self.max_x = get_min_max(ground.keys(), 'x')
        self.min_y, self.max_y = get_min_max(ground.keys(), 'y')
        self.x_start, self.x_end = self.min_x - 2, self.max_x + 6
        self.y_start, self.y_end = self.min_y - 1, self.max_y + 3
        self.fall_down_directions = {}

    def is_row_occupied(self, x, y):
        return self.is_ground(x, y) or self.is_full_water_row(x, y)

    def get_constrained_row(self, x, y):
        frontier = [(x, y)]
        visited = set()
        while frontier:
            next_cell = frontier.pop(0)

            if next_cell in self.ground:
                continue

            down = (next_cell[0], next_cell[1] + 1)
            if down not in self.ground and down not in self.water_tiles:
                return None

            if self.out_of_bounds(*next_cell):
                return None

            visited.add(next_cell)
            left = (next_cell[0] - 1, next_cell[1])
            right = (next_cell[0] + 1, next_cell[1])
            for cell in [left, right]:
                if cell not in visited:
                    frontier.append(cell)

        return visited

    def get_cell_in_edge_direction(self, x, y):
        frontier = [(x, y)]
        visited = set()
        while frontier:
            next_cell = frontier.pop(0)

            if next_cell in self.ground:
                continue

            down = (next_cell[0], next_cell[1] + 1)
            if down not in self.ground and down not in self.water_tiles:
                if down[0] < x:
                    return (x - 1, y)
                else:
                    return (x + 1, y)

            if self.out_of_bounds(*next_cell):
                return None

            visited.add(next_cell)
            left = (next_cell[0] - 1, next_cell[1])
            right = (next_cell[0] + 1, next_cell[1])
            for cell in [left, right]:
                if cell not in visited:
                    frontier.append(cell)

        return None

    def out_of_bounds(self, x, y):
        return not (self.min_x <= x <= self.max_x and self.min_y <= y <= self.max_y)

    def get_empty_space_in_row(self, x, y):
        row = self.get_constrained_row(x, y)
        if not row:
            return None
        return next(
            (cell for cell in row if cell not in self.ground and cell not in self.water_tiles),
            None
        )

    def is_full_water_row(self, x, y):
        row = self.get_constrained_row(x, y)
        if not row:
            return False

        return all(cell in self.water_tiles for cell in row)

    def is_ground(self, x, y):
        return self.ground.get(Coordinate(x, y)) == '#'


def main(screen, input_filename):
    with open(input_filename) as stream:
        clay_coordinates = parse_coordinates(stream.read().strip())

    ground = {}
    for coordinate in clay_coordinates:
        ground.update({
            Coordinate(*point): '#'
            for point in product(coordinate.x, coordinate.y)
        })

    ground = Ground(ground)
    frontier = [(500, ground.min_y)]
    second_frontier = []
    visited = set()
    last_draw = None
    while frontier:
        cell = frontier.pop(0)
        if ground.out_of_bounds(*cell):
            break

        visited.add(cell)

        x, y = cell
        down = (x, y + 1)
        if (
            down not in visited and
            down not in ground.ground
        ):
            frontier.append(down)

        sideways = (x - 1, y), (x + 1, y)
        for cell_to_add in sideways:
            if (
                cell_to_add not in visited and
                cell_to_add not in ground.ground and
                not ground.out_of_bounds(*cell_to_add)
            ):
                below_sideways = (cell_to_add[0], cell_to_add[1] + 1)
                if (
                    (down in ground.ground or down in visited) and
                    (below_sideways in ground.ground or below_sideways in visited)
                ):
                    frontier.append(cell_to_add)
                else:
                    second_frontier.append(cell_to_add)

        if not frontier:
            second_frontier = sorted(second_frontier, key=itemgetter(1), reverse=True)
            start_y = second_frontier[0][1]
            while second_frontier[0][1] == start_y:
                frontier.append(second_frontier.pop(0))

        time.sleep(0.001)
        if screen and (not last_draw or time.time() - last_draw > 0.25):
            last_draw = time.time()
            draw_flood_fill(ground, frontier, second_frontier, visited, screen)

    if screen:
        draw_flood_fill(ground, frontier, second_frontier, visited, screen)

    print 'Part 1:', len(visited)

    input('')

    # iteration = 0
    # while True:
    #     for drop in ground.water:
    #         if drop.still:
    #             continue

    #         if ground.is_row_occupied(drop.x, drop.y + 1):
    #             if ground.get_constrained_row(drop.x, drop.y):
    #                 drop.flowing = False
    #                 new_space = ground.get_empty_space_in_row(drop.x, drop.y)
    #                 if new_space:
    #                     drop.x, drop.y = new_space
    #             else:
    #                 drop.x, drop.y = ground.get_cell_in_edge_direction(drop.x, drop.y)
    #         else:
    #             drop.y += 1
    #             ground.water_tiles = {(drop.x, drop.y) for drop in ground.water}

    #     # Spawn new drop
    #     ground.water.append(Drop(500, 1))

    #     if any(ground.out_of_bounds(drop.x, drop.y) for drop in ground.water):
    #         break

    #     if screen:
    #         draw(ground, screen)

    #     time.sleep(0.25)
    #     iteration += 1

    print 'Part 2:', None


def draw(ground, screen):
    pad = curses.newpad(ground.y_end + 1, ground.x_end + 1)
    for x in range(ground.x_start, ground.x_end - 3):
        for y in range(ground.y_start, ground.y_end):
            pad.addch(y, x, '.')

    for p, value in ground.ground.iteritems():
        pad.addch(p.y, p.x, '#')

    for drop in ground.water:
        pad.addch(drop.y, drop.x, '|' if drop.flowing else '~')

    pad.addch(0, 500, '+')

    row_drops = {}
    for drop in ground.water:
        row_drops[drop.y] = row_drops.get(drop.y, 0) + 1
    for idx, row in row_drops.iteritems():
        pad.addstr(idx, ground.x_end - 3, str(row))

    pad.refresh(ground.y_start, ground.x_start, 0, 0, curses.LINES - 5, curses.COLS - 1)


def draw_flood_fill(ground, frontier, second_frontier, visited, screen):
    pad = curses.newpad(ground.y_end + 1, ground.x_end + 1)
    for x in range(ground.x_start, ground.x_end - 3):
        for y in range(ground.y_start, ground.y_end):
            pad.addch(y, x, '.')

    for p, value in ground.ground.iteritems():
        pad.addch(p.y, p.x, '#')

    for cell in frontier:
        pad.addch(cell[1], cell[0], '|')

    for cell in second_frontier:
        pad.addch(cell[1], cell[0], '{')

    for cell in visited:
        pad.addch(cell[1], cell[0], '~')

    pad.addch(0, 500, '+')

    pad.refresh(ground.y_start, ground.x_start, 0, 0, curses.LINES - 5, curses.COLS - 1)


def debug(stdscr):
    curses.nocbreak()
    stdscr.keypad(0)
    curses.echo()
    curses.endwin()
    import pdb; pdb.set_trace()


if __name__ == '__main__':
    if 'debug' in sys.argv:
        main(None, sys.argv[1])
    else:
        curses.wrapper(main, sys.argv[1])
