
import cProfile
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
        self.min_x, self.max_x = self.min_x - 1, self.max_x + 1
        self.min_y, self.max_y = get_min_max(ground.keys(), 'y')
        self.x_start, self.x_end = self.min_x - 2, self.max_x + 6
        self.y_start, self.y_end = self.min_y - 1, self.max_y + 3
        self.fall_down_directions = {}
        self.constrained_rows = {}

    def is_row_occupied(self, x, y):
        return self.is_ground(x, y) or self.is_full_water_row(x, y)

    def get_constrained_row(self, x, y, settled):
        frontier = set([(x, y)])
        visited = set()
        while frontier:
            next_cell = frontier.pop()
            visited.add(next_cell)

            left = (next_cell[0] - 1, next_cell[1])
            right = (next_cell[0] + 1, next_cell[1])
            for cell in [left, right]:
                if cell in self.ground:
                    continue

                if cell in self.constrained_rows:
                    return self.constrained_rows[cell]

                down = (cell[0], cell[1] + 1)
                if down not in self.ground and down not in settled:
                    return None

                if self.out_of_bounds(*cell):
                    return None

                if cell not in visited:
                    frontier.add(cell)

        for cell in visited:
            self.constrained_rows[cell] = visited

        return visited

    def is_stable_row(self, x, y, settled, flowing):
        frontier = [(x, y)]
        visited = set()
        while frontier:
            next_cell = frontier.pop(0)

            if next_cell in self.ground:
                continue

            if next_cell in self.constrained_rows:
                return self.constrained_rows[next_cell]

            down = (next_cell[0], next_cell[1] + 1)
            if down not in self.ground and down not in settled:
                return None

            if self.out_of_bounds(*next_cell):
                return None

            visited.add(next_cell)
            left = (next_cell[0] - 1, next_cell[1])
            right = (next_cell[0] + 1, next_cell[1])
            for cell in [left, right]:
                if cell not in visited:
                    frontier.append(cell)

        for cell in visited:
            self.constrained_rows[cell] = visited

        return visited

    def is_constrained_cube(self, x, y):
        frontier = [(x, y)]
        visited = set()
        while frontier:
            next_cell = frontier.pop(0)
            visited.add(next_cell)

            if next_cell in self.constrained_cubes:
                self.constrained_cubes.update(visited)
                return True

            to_add = [
                (next_cell[0], next_cell[1] + 1),
                (next_cell[0] - 1, next_cell[1]),
                (next_cell[0] + 1, next_cell[1])
            ]
            for cell in to_add:
                if self.out_of_bounds(*cell):
                    return False

                if cell not in visited and cell not in self.ground:
                    frontier.append(cell)
                    # frontier = sorted(frontier, key=itemgetter(1))

        self.constrained_cubes.update(visited)
        return True

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

    def update_settled(self, check_for_updates, flowing, settled, second_frontier):
        flowing_size_changed = True
        to_add = set()
        while flowing_size_changed:
            for cell in check_for_updates:
                if cell not in flowing:
                    continue

                if self.get_constrained_row(cell[0], cell[1], settled):
                    settled.add(cell)
                    to_add.update(self.neighbours(cell))
                    up_left = (cell[0] - 1, cell[1] - 1)
                    if up_left not in self.ground:
                        second_frontier.add(up_left)
                    up_right = (cell[0] + 1, cell[1] - 1)
                    if up_right not in self.ground:
                        second_frontier.add(up_right)

            check_for_updates.difference_update(settled)
            check_for_updates.update(to_add)
            len_flowing = len(flowing)
            flowing.difference_update(settled)
            flowing_size_changed = len_flowing != len(flowing)

        check_for_updates.clear()

    def neighbours(self, cell):
        return [
            (cell[0], cell[1] - 1),
            (cell[0] + 1, cell[1]),
            (cell[0] - 1, cell[1]),
        ]

    def update_frontier(self, frontier, second_frontier, flowing, settled):
        for cell in second_frontier:
            if cell in frontier or cell in flowing or cell in settled:
                continue

            if self.is_on_stable_ground(cell, flowing, settled):
                frontier.add(cell)
                continue

            if cell in self.ground:
                down_left = cell[0] - 1, cell[1]
                down_right = cell[0] + 1, cell[1]
                if any(
                    other in self.ground or other in settled
                    for other in [down_left, down_right]
                ):
                    frontier.add(cell)
                    continue

    def is_on_stable_ground(self, cell, flowing, settled):
        down = cell[0], cell[1] + 1
        if down not in self.ground and down not in settled:
            return False

        left = cell[0] - 1, cell[1]
        left_down = cell[0] - 1, cell[1] + 1
        if (left in flowing or left in settled) and (left_down in self.ground or left_down in settled):
            return True

        right = cell[0] + 1, cell[1]
        right_down = cell[0] + 1, cell[1] + 1
        if (right in flowing or right in settled) and (right_down in self.ground or right_down in settled):
            return True

        # row = self.get_constrained_row(down[0], down[1], settled)
        # return row and down in row


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

    settled = set()
    last_draw = None
    start_time = time.time()
    current_height = 0
    frontier = set([(500, 1)])
    second_frontier = set()
    check_for_updates = set()
    flowing = set()
    while frontier:
        cell = frontier.pop()
        if screen and not (current_height <= cell[1] <= current_height + curses.LINES):
            current_height = max(0, cell[1] - curses.LINES / 2)

        flowing.add(cell)
        check_for_updates.add(cell)

        x, y = cell
        down = (x, y + 1)
        if down not in flowing and down not in ground.ground and not ground.out_of_bounds(*down):
            frontier.add(down)

        sideways = (x - 1, y), (x + 1, y)
        for cell_to_add in sideways:
            if (
                cell_to_add not in flowing and
                cell_to_add not in ground.ground and
                not ground.out_of_bounds(*cell_to_add)
            ):
                if down in ground.ground:
                    frontier.add(cell_to_add)

        if not frontier:
            ground.update_settled(check_for_updates, flowing, settled, second_frontier)
            ground.update_frontier(frontier, second_frontier, flowing, settled)
            second_frontier.difference_update(frontier)
            if not frontier:
                break

            #     for cell in second_frontier:
            #         if down in second_frontier:
            #             continue

            #         if ground.is_constrained_cube(cell[0], cell[1] + 1):
            #             frontier.append(cell)
            #             second_frontier.remove(cell)

            # second_frontier = sorted(second_frontier, key=itemgetter(1), reverse=True)
            # start_y = second_frontier[0][1]
            # while second_frontier[0][1] == start_y:
            #     frontier.append(second_frontier.pop(0))

        if screen:
            time.sleep(0.50)
            if not last_draw or time.time() - last_draw > 0.25:
                last_draw = time.time()
                draw_flood_fill(ground, frontier, second_frontier, flowing, settled, screen, current_height)

    if screen:
        draw_flood_fill(ground, frontier, second_frontier, flowing, settled, screen, current_height)
        time.sleep(10)

    print 'Part 1:', len(flowing | settled)
    print 'Part 2:', len(settled)


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


def draw_flood_fill(ground, frontier, second_frontier, flowing, settled, screen, current_height):
    pad = curses.newpad(ground.y_end + 1, ground.x_end + 7)
    for x in range(ground.x_start, ground.x_end - 3):
        for y in range(ground.y_start, ground.y_end):
            pad.addch(y, x, '.')

    for p, value in ground.ground.iteritems():
        pad.addch(p.y, p.x, '#')

    for cell in frontier:
        pad.addch(cell[1], cell[0], '*')

    for cell in second_frontier:
        pad.addch(cell[1], cell[0], '{')

    for cell in flowing:
        pad.addch(cell[1], cell[0], '|')

    for cell in settled:
        pad.addch(cell[1], cell[0], '~')

    for y in range(ground.y_start, ground.y_end):
        pad.addstr(y, ground.x_end + 1, str(y))

    pad.addch(0, 500, '+')

    pad.refresh(current_height, ground.x_start, 0, 0, curses.LINES - 5, curses.COLS - 1)


def debug(stdscr):
    curses.nocbreak()
    stdscr.keypad(0)
    curses.echo()
    curses.endwin()
    import pdb; pdb.set_trace()


if __name__ == '__main__':
    if 'debug' in sys.argv:
        cProfile.run('main(None, sys.argv[1])')
    elif len(sys.argv) == 4 and sys.argv[2] == 'tofile':
        with open(sys.argv[1]) as stream:
            clay_coordinates = parse_coordinates(stream.read().strip())

        ground = {}
        for coordinate in clay_coordinates:
            ground.update({
                point: '#'
                for point in product(coordinate.x, coordinate.y)
            })

        min_x, max_x = get_min_max(ground.keys(), 0)
        min_y, max_y = get_min_max(ground.keys(), 1)

        with open(sys.argv[3], 'w') as stream:
            for y in range(min_y, max_y + 1):
                stream.write(''.join(
                    ['#' if (x, y) in ground else '.' for x in range(min_x, max_x + 1)]
                ) + '\n')

    elif 'noscreen' in sys.argv:
        main(None, sys.argv[1])
    else:
        curses.wrapper(main, sys.argv[1])
