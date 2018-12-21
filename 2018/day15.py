
import time
import cProfile
from collections import deque
import math
import sys
from operator import attrgetter

import curses


class Position(object):
    __slots__ = 'x', 'y', '_hash'

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self._hash = hash((self.x, self.y))

    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)

    def __hash__(self):
        return self._hash

    def __repr__(self):
        return str((self.x, self.y))


class Entity(object):
    def __init__(self, x, y, race):
        self.x = x
        self.y = y
        self.race = race
        self.hitpoints = 200
        self.is_alive = True

    @property
    def position(self):
        return Position(self.x, self.y)

    @property
    def sort_order(self):
        return self.y * 100 + self.x

    def move(self, position):
        self.x = position.x
        self.y = position.y


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
        self.ground_positions = set(key for key, value in graph.iteritems() if value == '.')
        self.entities = entities
        self.map_height = max(self.graph.keys(), key=attrgetter('y')).y
        self.map_width = max(self.graph.keys(), key=attrgetter('x')).x
        self.screen = screen
        self.flow_fields = {}

    def draw(self):
        # Map
        for coord, value in self.graph.iteritems():
            self.screen.addch(coord.y, coord.x, value)
        # Entities
        for idx, entity in enumerate(self.initiative_order()):
            self.screen.addch(entity.y, entity.x, entity.race)

        for idx, entity in enumerate(self.entities):
            self.screen.addstr(idx, self.map_width + 2, str(entity.hitpoints))

    @property
    def elves(self):
        return [entity for entity in self.entities if entity.race == 'E']

    @property
    def goblins(self):
        return [entity for entity in self.entities if entity.race == 'G']

    def step(self):
        for entity in self.initiative_order():
            if not entity.is_alive:
                continue

            self.elf_positions = {
                entity.position: entity for entity in self.elves if entity.is_alive
            }
            self.goblin_positions = {
                entity.position: entity for entity in self.goblins if entity.is_alive
            }
            self.occupied = set(self.elf_positions.keys() + self.goblin_positions.keys())
            self.valid_positions = self.ground_positions.difference(self.occupied)
            if not self.can_attack(entity):
                self.move(entity)

            self.attack(entity)

        self.entities = [entity for entity in self.entities if entity.is_alive]

    def can_attack(self, entity):
        if entity.race == 'G':
            return any(neighbour in self.elf_positions for neighbour in self.neighbours(entity))
        else:
            return any(neighbour in self.goblin_positions for neighbour in self.neighbours(entity))

    def move(self, entity):
        in_range = self.in_range(entity, self.enemies(entity))
        if not in_range:
            return
        chosen_in_range = self.closest(entity, in_range)
        if not chosen_in_range:
            return
        paths = sorted(
            self.paths_to(entity.position, chosen_in_range),
            key=lambda path: (path[0].y, path[0].x)
        )
        if paths:
            entity.move(paths[0][0])
            self.flow_fields = {}

    def attack(self, entity):
        enemies = self.elf_positions if entity.race == 'G' else self.goblin_positions
        try:
            target = sorted(
                [enemies[neighbour] for neighbour in self.neighbours(entity) if neighbour in enemies],
                key=attrgetter('hitpoints', 'y', 'x')
            )[0]
        except IndexError:
            return

        target.hitpoints -= 3
        if target.hitpoints <= 0:
            target.is_alive = False

    def enemies(self, entity):
        if entity.race == 'G':
            return self.elves
        else:
            return self.goblins

    def in_range(self, entity, targets):
        return [
            position
            for target in targets
            for position in self.neighbours(target.position)
            if position in self.valid_positions
        ]

    def closest(self, entity, positions):
        distances = {}
        min_distance = float('inf')
        for pos in positions:
            if not self.can_be_reached(entity.position, pos):
                continue
            distance = self.distance_to(entity.position, pos)
            distances.setdefault(distance, []).append(pos)
            min_distance = min(distance, min_distance)
        if not distances:
            return
        return min(distances.get(min_distance), key=attrgetter('y', 'x'))

    def distance_to(self, start, end):
        flow_field = self.get_flow_field(start)
        return flow_field.get(end, (None, None))[1]

    def can_be_reached(self, start, end):
        flow_field = self.get_flow_field(start)
        return end in flow_field

    def paths_to(self, start, end):
        def recursive(nodes, target):
            paths = []
            for parent in nodes[target][0]:
                child_paths = recursive(nodes, parent)
                if child_paths:
                    paths.extend([
                        [target] + child_path
                        for child_path in child_paths
                    ])
                else:
                    paths.append([target])
            return paths

        flow_field = self.get_flow_field(start)
        return [
            path[::-1]
            for path in recursive(flow_field, end)
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
                if neighbour not in self.valid_positions:
                    continue

                parents, distance = came_from.get(neighbour, ([], 999))
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
            Position(target.x, target.y - 1),
            Position(target.x + 1, target.y),
            Position(target.x, target.y + 1),
            Position(target.x - 1, target.y)
        ]


def main(screen, input_filename):
    with open(input_filename) as stream:
        cavern = Cavern.from_input(stream.read().strip(), screen)

    command = 'c'
    iterations = 0
    while True:
        if iterations == 32:
            debug(screen)
        loop_start = time.time()
        if screen:
            cavern.draw()
            if command != 'r':
                command = curses_raw_input(
                    screen, cavern.map_height + 2, '[C]ontinue / [S]top / [R]un: '
                ).lower()
            if command == 's':
                break
        cavern.step()
        time_diff = time.time() - loop_start
        if time_diff < 0.16:
            time.sleep(0.25 - time_diff)

        iterations += 1
        screen.addstr(cavern.map_height + 1, 0, 'Iteration {}'.format(iterations))
        screen.refresh()
        screen.clear()
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
    if 'debug' in sys.argv:
        cProfile.run('main(None, "{}")'.format(sys.argv[1]))
    elif 'no_screen' in sys.argv:
        main(None, sys.argv[1])
    else:
        curses.wrapper(main, sys.argv[1])
