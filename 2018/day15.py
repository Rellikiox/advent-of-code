
from collections import deque
import math
import sys
from itertools import groupby
from operator import attrgetter, itemgetter

import curses


class Position(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if isinstance(other, Position):
            return (self.x, self.y) == (other.x, other.y)
        return False

    def __hash__(self):
        return hash((self.x, self.y))

    def __repr__(self):
        return str((self.x, self.y))


class Entity(object):
    def __init__(self, x, y, race):
        self.x = x
        self.y = y
        self.race = race

    @property
    def position(self):
        return Position(self.x, self.y)

    @property
    def sort_order(self):
        return self.y * 100 + self.x


class Cavern(object):
    @classmethod
    def from_input(cls, map_data, screen):
        entities = []
        graph = {}
        for y, row in enumerate(map_data.split('\n')):
            for x, cell_value in enumerate(row.strip()):
                if cell_value == 'G' or cell_value == 'E':
                    entities.append(Entity(x, y, cell_value))
                    graph[Position(x, y)] = '.'
                else:
                    graph[Position(x, y)] = cell_value

        return cls(graph, entities, screen)

    def __init__(self, graph, entities, screen):
        self.graph = graph
        self.entities = entities
        self.map_height = max(coord.y for coord in self.graph.keys())
        self.screen = screen
        self.flow_fields = {}

    def draw(self):
        self.screen.clear()

        # Map
        for coord, value in self.graph.iteritems():
            self.screen.addch(coord.y, coord.x, value)
        # Entities
        for idx, entity in enumerate(self.initiative_order()):
            self.screen.addch(entity.y, entity.x, entity.race)
        # In Range
        in_range = self.in_range(self.elves[0], self.goblins)
        for position in in_range:
            self.screen.addch(position.y, position.x, '?')
        # Closest
        chosen_in_range = self.closest(self.elves[0], in_range)
        self.screen.addch(chosen_in_range.y, chosen_in_range.x, '!', curses.A_BOLD)

        paths = sorted(
            self.paths_to(self.elves[0].position, chosen_in_range),
            key=lambda path: (path[0].y, path[0].x)
        )
        for step in paths[0]:
            self.screen.addch(step.y, step.x, 'x')

        self.screen.refresh()

    @property
    def elves(self):
        return [entity for entity in self.entities if entity.race == 'E']

    @property
    def goblins(self):
        return [entity for entity in self.entities if entity.race == 'G']

    def in_range(self, entity, targets):
        return [
            position
            for target in targets
            for position in self.neighbours(target.position)
            if self.is_valid(position)
        ]

    def closest(self, entity, positions):
        cosest_nodes = [
            position_pair[0]
            for position_pair in next(
                groupby(
                    sorted(
                        [
                            (position, self.distance_to(entity.position, position))
                            for position in positions
                            if self.can_be_reached(entity.position, position)
                        ],
                        key=itemgetter(1)
                    ),
                    key=itemgetter(1)
                )
            )[1]
        ]
        return min(cosest_nodes, key=attrgetter('y', 'x'))

    def distance_to(self, start, end):
        flow_field = self.get_flow_field(start)
        return flow_field.get(end, (None, None))[1]

    def can_be_reached(self, start, end):
        flow_field = self.get_flow_field(start)
        return end in flow_field

    def paths_to(self, start, end):
        def recursive(nodes, target, start):
            paths = []
            for parent in nodes[target][0]:
                if parent == start:
                    continue
                child_paths = recursive(nodes, parent, start)
                if child_paths:
                    paths.extend([
                        [parent] + child_path
                        for child_path in child_paths
                    ])
                else:
                    paths.append([parent])
            return paths

        flow_field = self.get_flow_field(start)
        return [
            path[::-1]
            for path in recursive(flow_field, end, start)
        ]

    def get_flow_field(self, start):
        if start not in self.flow_fields:
            self.flow_fields[start] = self.make_flow_field(start)
        return self.flow_fields[start]

    def make_flow_field(self, start):
        frontier = deque()
        frontier.append((start, 0))
        came_from = {}
        came_from[start] = [], 0

        while frontier:
            current, node_distance = frontier.popleft()
            new_distance = node_distance + 1
            for neighbour in self.neighbours(current):
                if not self.is_valid(neighbour):
                    continue

                parents, distance = came_from.get(neighbour, ([], float('inf')))
                if new_distance <= distance and current not in parents:
                    frontier.append((neighbour, new_distance))
                    parents.append(current)
                    came_from[neighbour] = parents, new_distance

        return came_from

    def distance(self, entity_position, position):
        return int(
            math.fabs(entity_position.x + position.x) +
            math.fabs(entity_position.y + position.y)
        )

    def initiative_order(self):
        return sorted(self.entities, key=attrgetter('sort_order'))

    def neighbours(self, target):
        return [
            position for position in [
                Position(target.x + change[0], target.y + change[1])
                for change in [(0, -1), (1, 0), (0, 1), (-1, 0)]
            ]
            if self.is_valid(position)
        ]

    def is_valid(self, position):
        return (
            self.graph[position] != '#' and
            position not in [entity.position for entity in self.entities]
        )


def main(screen, input_filename):
    with open(input_filename) as stream:
        cavern = Cavern.from_input(stream.read().strip(), screen)

    cavern.draw()

    curses_raw_input(screen, cavern.map_height + 5, 'Close?')
    print 'Part 1:', None
    print 'Part 2:', None


def curses_raw_input(stdscr, y, prompt_string):
    curses.echo()
    stdscr.addstr(y, 0, prompt_string)
    stdscr.refresh()
    input = stdscr.getstr(y + 1, 0, 20)
    return input


def debug(stdscr):
    curses.nocbreak()
    stdscr.keypad(0)
    curses.echo()
    curses.endwin()
    import pdb; pdb.set_trace()


if __name__ == '__main__':
    curses.wrapper(main, sys.argv[1])
