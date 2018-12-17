
from __future__ import print_function

from Queue import deque
import math
from operator import attrgetter
import sys


class Node(object):
    def __init__(self, coordinates, label, is_origin):
        self.coordinates = coordinates
        self.label = label
        self.is_origin = is_origin
        self.distance = 0 if is_origin else float('inf')
        self.contested = False

    @property
    def x(self):
        return self.coordinates[0]

    @property
    def y(self):
        return self.coordinates[1]

    def claim(self, other_node):
        if other_node.is_origin:
            return False

        distance = self.distance + 1
        if distance < other_node.distance:
            other_node.label = self.label
            other_node.distance = distance
            return True
        elif distance == other_node.distance:
            if self.label != other_node.label:
                other_node.contested = True
            return False

        return False

    def neighbours(self):
        return [
            (self.x - 1, self.y),
            (self.x, self.y - 1),
            (self.x + 1, self.y),
            (self.x, self.y + 1)
        ]

    def manhatan_distance(self, other):
        return math.fabs(self.x - other.x) + math.fabs(self.y - other.y)


#     with open(input_file) as stream:
#         coordinates = {}
#         for idx, line in enumerate(stream):
#             x, y = line.split(', ')
#             x, y = int(x.strip()), int(y.strip())
#             coordinates[(x, y)] = Coordinate(x, y, chr(idx + 65))

#     boundaries = (
#         (
#             min([coord for coord in coordinates.values()], key=attrgetter('x')).x,
#             max([coord for coord in coordinates.values()], key=attrgetter('x')).x
#         ),
#         (
#             min([coord for coord in coordinates.values()], key=attrgetter('y')).y,
#             max([coord for coord in coordinates.values()], key=attrgetter('y')).y
#         )
#     )
#     destination_map = {}

#     for i in x_range(boundaries):
#         for j in y_range(boundaries):
#             destination_map[(i, j)] = Cell('', False, False)

#     for key, val in coordinates.iteritems():
#         destination_map[key] = Cell(val.idx, False, True)

#     for key, cell_value in destination_map.iteritems():
#         if cell_value.is_origin:
#             continue

#         origin_distances = [
#             (origin, manhatan_distance(origin, key))
#             for origin in coordinates.values()
#         ]
#         min_distance = min(distance[1] for distance in origin_distances)
#         origins_in_destination = [
#             origin[0].idx
#             for origin in origin_distances
#             if origin[1] == min_distance
#         ]
#         if len(origins_in_destination) == 1:
#             destination_map[key] = Cell(origins_in_destination[0].idx, False, False)
#         else:
#             destination_map[key] = Cell(None, True, False)

#     # origins_in_infinite = set(
#     #     destination_map[i][0]
#     #     for i in x_range(boundaries)
#     # ) +  set(
#     #     for j in y_range(boundaries)
#     # )


# def x_range(boundaries):
#     return range(boundaries[0][0], boundaries[0][1] + 1)


# def y_range(boundaries):
#     return range(boundaries[1][0], boundaries[1][1] + 1)


def main(input_file):
    with open(input_file) as stream:
        origins = []
        for idx, line in enumerate(stream):
            x, y = [int(val.strip()) for val in line.split(', ')]
            label = chr(idx + 65)
            origins.append(Node((x, y), label, True))

    boundaries = (
        (
            min([node for node in origins], key=attrgetter('x')).x,
            max([node for node in origins], key=attrgetter('x')).x
        ),
        (
            min([node for node in origins], key=attrgetter('y')).y,
            max([node for node in origins], key=attrgetter('y')).y
        )
    )

    # part_1 = largest_bound_region(origins, boundaries)
    # print('Part 1:', part_1)
    part_2 = largest_safe_region(origins, boundaries)
    print('Part 1:', part_2)


def largest_bound_region(origins, boundaries):
    destination_map = {}
    for x in x_range(boundaries):
        for y in y_range(boundaries):
            destination_map[(x, y)] = Node((x, y), '', False)
    for origin in origins:
        destination_map[origin.coordinates] = origin

    eligible_origins = {origin.label for origin in origins}
    open_set = deque([origin.coordinates for origin in origins])
    while open_set:
        node = destination_map.get(open_set.popleft())
        for neighbour_coordinates in node.neighbours():
            if out_of_bounds(neighbour_coordinates, boundaries):
                try:
                    eligible_origins.remove(node.label)
                except KeyError:
                    pass
            else:
                other_node = destination_map.get(neighbour_coordinates)
                claimed = node.claim(other_node)
                if claimed:
                    open_set.append(neighbour_coordinates)

    claimed_locations = [
        _node.label
        for _node in destination_map.values()
        if not _node.contested and _node.label in eligible_origins
    ]
    return max(claimed_locations.count(label) for label in eligible_origins)


def largest_safe_region(origins, boundaries):
    safe_region_count = 0
    destination_map = {}
    for x in x_range(boundaries):
        for y in y_range(boundaries):
            total_distances = sum(
                math.fabs(origin.x - x) + math.fabs(origin.y - y)
                for origin in origins
            )
            destination_map[(x, y)] = total_distances
            safe_region_count += total_distances < 10000

    # for i in x_range(boundaries):
    #     for j in y_range(boundaries):
    #         print_value = '#' if destination_map[(i, j)] < 10000 else '.'
    #         print(print_value, end='  ')
    #     print('\n')

    return safe_region_count


def x_range(boundaries):
    return range(boundaries[0][0], boundaries[0][1] + 1)


def y_range(boundaries):
    return range(boundaries[1][0], boundaries[1][1] + 1)


def out_of_bounds(coordinates, boundaries):
    return (
        coordinates[0] < boundaries[0][0] or coordinates[0] > boundaries[0][1] or
        coordinates[1] < boundaries[1][0] or coordinates[1] > boundaries[1][1]
    )


if __name__ == '__main__':
    main(sys.argv[1])
