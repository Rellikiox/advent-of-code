
import argparse
import itertools


def main():
    parser = argparse.ArgumentParser(description='Advent of code day 9')
    parser.add_argument('input', metavar='I', help='File wiht the input data')

    args = parser.parse_args()
    if args.input:
        with open(args.input, 'r') as input_file:
            lines = [line.strip() for line in input_file]
            nodes = get_nodes(lines)
            print find_shortest(nodes)


def get_nodes(inputs):
    nodes = {}
    for route in inputs:
        start, end, length = parse_line(route)
        nodes.setdefault(start, {})[end] = int(length)
        nodes.setdefault(end, {})[start] = int(length)
    return nodes


def parse_line(route):
    start, rest = route.split(' to ')
    end, length = rest.split(' = ')
    return start, end, length


def find_shortest(nodes):
    all_routes = itertools.permutations(nodes.keys())
    shortest = None
    for route in all_routes:
        route_length = calculate_route_length(route, nodes)
        if not shortest or route_length < shortest:
            shortest = route_length
    return shortest


def calculate_route_length(route, nodes):
    length = 0
    for i in range(len(route) - 1):
        start, end = route[i:i+2]
        length += nodes[start][end]
    return length


if __name__ == '__main__':
    main()
