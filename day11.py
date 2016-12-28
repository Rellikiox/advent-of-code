
from collections import namedtuple
import copy
import re

simple_input = """The first floor contains a hydrogen-compatible microchip.
The second floor contains nothing relevant."""
simple_input_with_gen = """The first floor contains a hydrogen-compatible microchip.
The second floor contains a hydrogen generator.
The thirdd floor contains nothing relevant."""
simple_input_with_gen_extra = """The first floor contains a hydrogen-compatible microchip and a lithium-compatible microchip.
The second floor contains a hydrogen generator.
The thirdd floor contains a lithium generator."""

test_input = """The first floor contains a hydrogen-compatible microchip and a lithium-compatible microchip.
The second floor contains a hydrogen generator.
The third floor contains a lithium generator.
The fourth floor contains nothing relevant."""

microchip_re = r'a (\w+)-compatible microchip'
generator_re = r'a (\w+) generator'


class State(object):
    Floor = namedtuple('Floor', ['microchips', 'generators'])
    Action = namedtuple('Action', ['origin', 'dest', 'items'])

    def __init__(self, floors, current_floor, steps):
        self.floors = copy.deepcopy(floors)
        self.current_floor = current_floor
        self.steps = steps

    @classmethod
    def from_action(cls, state, action):
        new_state = cls(state.floors, state.current_floor, state.steps)
        new_state.do_action(action)
        return new_state

    @classmethod
    def from_rules(cls, rules):
        def items_in_rule(rule):
            microchips = re.findall(microchip_re, rule) or []
            generators = re.findall(generator_re, rule) or []
            return [m[0].upper() for m in microchips], [g[0].upper() for g in generators]

        floors = [cls.Floor(*items_in_rule(rule)) for rule in rules if rule.strip()]

        return cls(floors, 0, 0)

    def is_final_state(self):
        return all(
            not floor.microchips and not floor.generators
            for floor in self.floors[:-1]
        )

    def do_action(self, action):
        for item in action.items:
            item_name = item[1:]
            if 'm' in item:
                self.floors[action.origin].microchips.remove(item_name)
                self.floors[action.dest].microchips.append(item_name)
            else:
                self.floors[action.origin].generators.remove(item_name)
                self.floors[action.dest].generators.append(item_name)

        self.current_floor = action.dest
        self.steps += 1

    def get_posible_states(self):
        # Get floors I can move to
        adjacent_floors = [
            floor_idx for floor_idx in range(len(self.floors))
            if abs(floor_idx - self.current_floor) == 1
        ]
        # Get items I can take with me
        actions = self.get_posible_actions(adjacent_floors)

        posible_states = []
        for action in actions:
            # For each action create a new world state
            new_state = State.from_action(self, action)
            # If it's valid return it
            if new_state.is_valid_state():
                posible_states.append(new_state)

        return posible_states

    def is_valid_state(self):
        is_valid = (
            all(
                not floor.generators or m in floor.generators
                for floor in self.floors
                for m in floor.microchips
            ) or
            all(
                not floor.microchips or g in floor.microchips
                for floor in self.floors
                for g in floor.generators
            )
        )
        # print is_valid, self.hash()
        return is_valid

    def get_posible_actions(self, adjacent_floors):
        movable_items = [[item] for item in self.items_in_floor(self.current_floor)]

        for m in self.floors[self.current_floor].microchips:
            if m in self.floors[self.current_floor].generators:
                movable_items.append(['m{}'.format(m), 'g{}'.format(m)])

        # Get list of posible actions
        actions = [
            State.Action(self.current_floor, floor_idx, item_list)
            for floor_idx in adjacent_floors
            for item_list in movable_items
        ]

        return actions

    def hash(self):
        """0:mH.mL-gH-gL"""
        return '{}:{}'.format(
            self.current_floor,
            '-'.join([
                '.'.join(sorted(self.items_in_floor(floor_idx)))
                for floor_idx in range(len(self.floors))
            ])
        )

    def items_in_floor(self, floor_id):
        return (
            ['m{}'.format(microchip) for microchip in self.floors[floor_id].microchips] +
            ['g{}'.format(generator) for generator in self.floors[floor_id].generators]
        )

    def __repr__(self):
        indexed_floors = [f for f in enumerate(self.floors)]
        all_items = sorted(list(set([
            item
            for floor_idx in range(len(self.floors))
            for item in self.items_in_floor(floor_idx)
        ])))
        floor_str = '\n'.join([
            '{}{} {}'.format(
                floor_idx,
                '&' if self.current_floor == floor_idx else ' ',
                '  '.join(item if item in self.items_in_floor(floor_idx) else '  ' for item in all_items)
            )
            for floor_idx, floor in reversed(indexed_floors)
        ])
        return """--- step {} ---
{}
----------""".format(self.steps, floor_str)


def steps_to_fourth_floor(input):
    available_states = [State.from_rules(input.split('\n'))]
    visited_states = set()

    states_processed = 0
    while available_states:
        state = available_states.pop(0)
        # print state
        if state.hash() in visited_states:
            continue
        if state.is_final_state():
            return state

        available_states.extend(state.get_posible_states())

        visited_states.add(state.hash())
        states_processed += 1
        if states_processed % 10000 == 0:
            print states_processed

    return None


def main():
    state = steps_to_fourth_floor(test_input)
    if state:
        print '###### FINAL STATE FOUND ######'
        print state
    else:
        print '###### NO FINAL STATE FOUND ######'


if __name__ == '__main__':
    main()
