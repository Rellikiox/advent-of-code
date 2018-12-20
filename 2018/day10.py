
from operator import itemgetter
import sys
import re


coordinate_re = re.compile(r'position=<\s*([^,]+),\s*([^>]+)> velocity=<\s*([^,]+),\s*([^>]+)>')


def main(input_filename):
    with open(input_filename) as stream:
        points = [
            [int(val) for val in coordinate_re.match(line.strip()).groups()]
            for line in stream
        ]

    n_steps = 0
    command = 'y'
    while command != 'n':
        if points_are_closeish(points):
            display(points)
            command = raw_input('Continue? (y/n)')[0]
            print n_steps
        points = step(points)
        n_steps += 1


def display(points):
    min_x = min(points, key=itemgetter(0))[0]
    max_x = max(points, key=itemgetter(0))[0]
    x_diff = max_x - min_x
    min_y = min(points, key=itemgetter(1))[1]
    max_y = max(points, key=itemgetter(1))[1]
    y_diff = max_y - min_y

    point_matrix = [['.'] * (x_diff + 1) for _ in range(y_diff + 1)]
    x_displace, y_displace = 0 - min_x, 0 - min_y
    for point in points:
        x, y = point[:2]
        transformed_x, transformed_y = x + x_displace, y + y_displace
        point_matrix[transformed_y][transformed_x] = '#'

    print '\n'.join([' '.join(point_row) for point_row in point_matrix])


def points_are_closeish(points):
    min_y = min(points, key=itemgetter(1))[1]
    max_y = max(points, key=itemgetter(1))[1]
    y_diff = max_y - min_y
    return y_diff < 10


def step(points):
    for point in points:
        point[0] += point[2]
        point[1] += point[3]
    return points


if __name__ == '__main__':
    main(sys.argv[1])
