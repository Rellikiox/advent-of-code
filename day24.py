
import itertools


test_input = (
    '###########\n'
    '#0.1.....2#\n'
    '#.#######.#\n'
    '#4.......3#\n'
    '###########'
)
test_output = 14


def main():
    # Create and initialize a map
    # map_data = test_input.split('\n')
    map_data = open('day24input.txt').read().split('\n')
    nodes = {}
    number_locations = {}
    for row_idx, row in enumerate(map_data):
        for col_idx, cell in enumerate(row):
            if cell != '#':
                neighbours = [
                    (i, j)
                    for i, j in (
                        (row_idx - 1, col_idx), (row_idx, col_idx + 1),
                        (row_idx + 1, col_idx), (row_idx, col_idx - 1)
                    )
                    if i < len(map_data) and j < len(row) and map_data[i][j] != '#'
                ]
                nodes[(row_idx, col_idx)] = neighbours

                if cell != '.':
                    number_locations[cell] = (row_idx, col_idx)

    # Calculate shortest path lengths between pairs of points
    target_numbers = number_locations.keys()
    sub_paths = {}
    for two_node_path in itertools.combinations(target_numbers, 2):
        origin = number_locations[two_node_path[0]]
        target = number_locations[two_node_path[1]]
        frontier = list()
        visited = set()

        frontier.append((origin, 0))
        nodes_checked = 0
        while frontier:
            current_node, path_length = frontier.pop(0)
            if current_node in visited:
                continue

            # Check goal state
            if current_node == target:
                sub_paths[two_node_path] = path_length
                break

            for neighbour_node in nodes[current_node]:
                if neighbour_node in visited:
                    continue
                else:
                    frontier.append((neighbour_node, path_length + 1))
            nodes_checked += 1
            visited.add(current_node)
    print sub_paths

    # Calculate shortest sum of steps for all combinations of paths
    min_path = float('inf')
    target_numbers.remove('0')
    for possible_path in itertools.permutations(target_numbers):
        possible_path = ('0',) + possible_path
        path_length = 0
        for i in range(len(possible_path) - 1):
            number_pair = (possible_path[i], possible_path[i + 1])
            if number_pair not in sub_paths:
                number_pair = tuple(reversed(number_pair))
            path_length += sub_paths[number_pair]

        min_path = min(min_path, path_length)

    print 'Shortest path is:', min_path


if __name__ == '__main__':
    main()
