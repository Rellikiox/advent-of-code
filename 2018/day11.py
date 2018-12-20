
from itertools import product
import sys

grid_width = 300


def main(grid_serial_number, max_grid_size):

    grid = {
        (x, y): get_power_level(x, y, grid_serial_number)
        for x, y in product(range(grid_width), range(grid_width))
    }

    memory = {
        (coord[0], coord[1], 1): power_level
        for coord, power_level in grid.iteritems()
    }

    max_power_level = float('-inf')
    max_power_coord = (None, None, None)
    for grid_size in range(2, max_grid_size + 1):
        for x, y in product(range(grid_width - grid_size + 1), range(grid_width - grid_size + 1)):

            # grid_coordinates = zip(range(x, x + grid_size), range(y, y + grid_size))
            grid_coordinates = set(
                zip([x + grid_size - 1] * grid_size, range(y, y + grid_size)) +
                zip(range(x, x + grid_size), [y + grid_size - 1] * grid_size)
            )
            grid_power_level = sum(grid[coord] for coord in grid_coordinates) + memory[x, y, grid_size - 1]
            memory[x, y, grid_size] = grid_power_level
            if grid_power_level > max_power_level:
                max_power_level = grid_power_level
                max_power_coord = (x, y, grid_size)

        # print '({}, {}) = {}'.format(x, y, grid_power_level)

    print 'Max ({}, {}, {}) = {}'.format(
        max_power_coord[0] + 1, max_power_coord[1] + 1, max_power_coord[2], max_power_level
    )

    # print '\n'.join(
    #     ''.join(['% 3d' % grid[x, y] for x in range(grid_width)])
    #     for y in range(grid_width)
    # )


def get_power_level(x, y, serial):
    x += 1
    y += 1
    # Find the fuel cell's rack ID, which is its X coordinate plus 10.
    rack_id = x + 10
    # Begin with a power level of the rack ID times the Y coordinate.
    power_level = rack_id * y
    # Increase the power level by the value of the grid serial number (your puzzle input).
    power_level += serial
    # Set the power level to itself multiplied by the rack ID.
    power_level *= rack_id
    # Keep only the hundreds digit of the power level (so 12345 becomes 3;
    # numbers with no hundreds digit become 0).
    power_level = int(str(power_level)[-3]) if power_level >= 100 else 0
    # Subtract 5 from the power level.
    power_level -= 5
    return power_level


if __name__ == '__main__':
    main(int(sys.argv[1]), int(sys.argv[2]))
