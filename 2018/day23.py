
from Queue import PriorityQueue
import math
import re
import sys
from itertools import product
from operator import attrgetter

bot_re = re.compile(r'pos=<(-?\d+),(-?\d+),(-?\d+)>, r=(-?\d+)')


def to_int(values):
    return [int(value) for value in values]


def min_max_diff(elements, attr):
    min_value = getattr(min(elements, key=attrgetter(attr)), attr)
    max_value = getattr(max(elements, key=attrgetter(attr)), attr)
    diff_value = max_value - min_value
    return min_value, max_value, diff_value


class Bot(object):
    def __init__(self, x, y, z, r):
        self.x = x
        self.y = y
        self.z = z
        self.r = r

    def distance(self, other):
        return int(
            math.fabs(self.x - other.x) +
            math.fabs(self.y - other.y) +
            math.fabs(self.z - other.z)
        )

    def in_range(self, other):
        return self.distance(other) <= self.r


class OctoSearch(object):
    def __init__(self, elements):
        self.elements = elements
        self.min_x, self.max_x, self.diff_x = min_max_diff(elements, 'x')
        self.min_y, self.max_y, self.diff_y = min_max_diff(elements, 'y')
        self.min_z, self.max_z, self.diff_z = min_max_diff(elements, 'z')
        max_diff = max(self.diff_x, self.diff_y, self.diff_z)
        self.depth_levels = range(1, int(math.ceil(math.log(max_diff, 2))) + 1)

    def best_quadrant(self, level):
        for x, y, z in self.quadrant_coords(level):
            print x, y, z

    def quadrant_coords(self, level, sub_quadrant):
        x_factor, y_factor, z_factor = self.diff_x / level, self.diff_y / level, self.diff_z / level
        range_x = ((self.min_x + x * x_factor) for x in xrange(2 ** level))
        range_y = ((self.min_y + y * y_factor) for y in xrange(2 ** level))
        range_z = ((self.min_z + z * z_factor) for z in xrange(2 ** level))
        return product(range_x, range_y, range_z)


def main(input_filename):
    with open(input_filename) as stream:
        bots = [Bot(*to_int(bot_re.match(line).groups())) for line in stream]

    best_bot = max(bots, key=attrgetter('r'))
    in_range = [
        bot for bot in bots if best_bot.in_range(bot)
    ]
    print 'Part 1:', len(in_range)

    search = OctoSearch(bots)
    print search.best_quadrant(1)
    print 'Part 2:', None


if __name__ == '__main__':
    main(sys.argv[1])
