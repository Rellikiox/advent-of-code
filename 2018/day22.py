
import math
import sys
from heapq import heapify, heappop, heappush
from itertools import product


def parse_input(input_filename):
    with open(input_filename) as stream:
        raw_depth, raw_target = stream.read().strip().split('\n')
    depth = int(raw_depth.split(' ')[1])
    target = tuple([int(value) for value in raw_target.split(' ')[1].split(',')])

    return depth, target


def geo_index(pos, cave, erosion):
    # The region at 0,0 (the mouth of the cave) has a geologic index of 0.
    # The region at the coordinates of the target has a geologic index of 0.
    if pos in cave:
        return cave[pos]
    # If the region's Y coordinate is 0, the geologic index is its X coordinate times 16807.
    if pos[1] == 0:
        return pos[0] * 16807
    # If the region's X coordinate is 0, the geologic index is its Y coordinate times 48271.
    if pos[0] == 0:
        return pos[1] * 48271
    # Otherwise, the region's geologic index is the result of multiplying the erosion levels of
    # the regions at X-1,Y and X,Y-1.
    return erosion[(pos[0] - 1, pos[1])] * erosion[(pos[0], pos[1] - 1)]


def erosion_level(geo_index, cave_depth):
    return (geo_index + cave_depth) % 20183


def risk_level(section_type, corner):
    return sum(
        section_type[pos]
        for pos in product(range(corner[0] + 1), range(corner[1] + 1))
    )


class Node(object):
    def __init__(self, tool, coord):
        self.tool = tool
        self.coord = coord
        self.neighbours = set()

    def add_neighbours(self, neighbours):
        self.neighbours.update(neighbours)
        for neighbour in neighbours:
            neighbour.neighbours.add(self)

    def __hash__(self):
        return hash((self.coord[0], self.coord[1], self.tool))


class AStar(object):
    def __init__(self, cave_data, start, end):
        section_to_tool = {0: 'tc', 1: 'cn', 2: 'tn'}
        self.nodes_by_coord = {}
        for coord, section in cave_data.iteritems():
            node_a, node_b = [Node(tool, coord) for tool in section_to_tool[section]]
            node_a.add_neighbours([node_b])
            self.nodes_by_coord[coord] = [node_a, node_b]

        start_node, end_node = Node('t', start), Node('t', end)
        start_node.add_neighbours(self.nodes_by_coord[start])
        self.nodes_by_coord[start].append(start_node)
        end_node.add_neighbours(self.nodes_by_coord[end])
        self.nodes_by_coord[end].append(end_node)

        for coord, nodes in self.nodes_by_coord.iteritems():
            neighbours = self.get_neighbours(coord)
            for node in nodes:
                neighbours_of_node = [
                    neighbour
                    for neighbour in neighbours
                    if neighbour.tool == node.tool
                ]
                node.add_neighbours(neighbours_of_node)

    def get_neighbours(self, coord):
        neighbour_coords = [
            (coord[0], coord[1] - 1),
            (coord[0] + 1, coord[1]),
            (coord[0], coord[1] + 1),
            (coord[0] - 1, coord[1])
        ]
        return [
            neighbour
            for _coord in neighbour_coords
            for neighbour in self.nodes_by_coord.get(_coord, [])
        ]

    def cost(self, node_a, node_b):
        return 1 if node_a.tool == node_b.tool else 7

    def heuristic(self, node_a, node_b):
        return int(
            math.fabs(node_a.coord[0] - node_b.coord[0]) +
            math.fabs(node_a.coord[1] - node_b.coord[1])
        )

    def cost_of_path_to(self, start, end):
        frontier = []
        heapify(frontier)
        heappush(frontier, (0, start))
        came_from = {}
        cost_so_far = {}
        came_from[start] = None
        cost_so_far[start] = 0

        while frontier:
            cost, current = heappop(frontier)

            if current == end:
                break

            for neighbour in current.neighbours:
                new_cost = cost_so_far[current] + self.cost(current, neighbour)
                if neighbour not in cost_so_far or new_cost < cost_so_far[neighbour]:
                    cost_so_far[neighbour] = new_cost
                    priority = new_cost + self.heuristic(end, neighbour)
                    heappush(frontier, (priority, neighbour))
                    came_from[neighbour] = current

        return cost_so_far[end]

    def get_start_end(self, start, end):
        start_node = next(node for node in self.nodes_by_coord[start] if node.tool == 't')
        end_node = next(node for node in self.nodes_by_coord[end] if node.tool == 't')
        return start_node, end_node


def main(input_filename, print_cave):
    depth, target = parse_input(input_filename)

    cave = {
        (0, 0): 0,
        target: 0
    }
    erosion_chars = ['.', '=', '|']
    erosion = {}
    section_type = {}
    action_range = target[0] * 10, target[1] * 2
    for x in range(action_range[0] + 1):
        for y in range(action_range[1] + 1):
            cave[(x, y)] = geo_index((x, y), cave, erosion)
            erosion[(x, y)] = erosion_level(cave[(x, y)], depth)
            section_type[(x, y)] = erosion[(x, y)] % 3

    if print_cave:
        for y in range(action_range[1] + 1):
            print ''.join(erosion_chars[section_type[(x, y)]] for x in range(action_range[0] + 1))

    print 'Part 1:', risk_level(section_type, target)

    astar = AStar(section_type, (0, 0), target)
    start_node, end_node = astar.get_start_end((0, 0), target)
    print 'Part 2:', astar.cost_of_path_to(start_node, end_node)


if __name__ == '__main__':
    main(sys.argv[1], 'print' in sys.argv)
