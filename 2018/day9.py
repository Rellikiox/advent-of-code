
from __future__ import print_function

from itertools import cycle
import sys


class Node:
    def __init__(self, value, prev_node=None, next_node=None):
        self.value = value
        self.prev_node = prev_node
        self.next_node = next_node


def play_game(n_players, n_marbles):
    circle = Node(0)
    circle.next_node = circle
    circle.prev_node = circle
    current_marble = circle

    next_marble_value = 1
    player_scores = [0] * n_players
    players = cycle(range(n_players))
    for player in players:
        if next_marble_value > n_marbles:
            break

        if next_marble_value % 23 == 0:
            node_to_delete = current_marble.prev_node.prev_node.prev_node.prev_node.prev_node.prev_node.prev_node
            node_to_delete.prev_node.next_node, node_to_delete.next_node.prev_node = node_to_delete.next_node, node_to_delete.prev_node
            current_marble = node_to_delete.next_node
            player_scores[player] += next_marble_value + node_to_delete.value
        else:
            new_node = Node(
                next_marble_value,
                current_marble.next_node,
                current_marble.next_node.next_node
            )
            current_marble.next_node.next_node.prev_node = new_node
            current_marble.next_node.next_node = new_node
            current_marble = new_node

        next_marble_value += 1

    return max(player_scores)


def main(n_players, n_marbles):
    print('Part 1:', play_game(n_players, n_marbles))
    print('Part 2:', play_game(n_players, n_marbles * 100))


def print_current_play(circle, current_marble, current_player):
    values_to_print = [('% 4d' % circle.value)]
    print_node = circle.next_node
    while print_node is not circle:
        if print_node is current_marble:
            values_to_print.append('({})'.format(print_node.value).rjust(4, ' '))
        else:
            values_to_print.append(('% 4d' % print_node.value))
        print_node = print_node.next_node

    print('[{}]'.format(current_player), ' '.join(values_to_print))


if __name__ == '__main__':
    main(int(sys.argv[1]), int(sys.argv[2]))
