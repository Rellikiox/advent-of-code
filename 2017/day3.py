import math

square_id = 289326


def dist_to_center(target):

    layer_side = math.ceil(math.sqrt(target))
    if layer_side % 2 == 0:
        layer_side += 1
    layer_number = (layer_side - 1) / 2

    layer_start = math.pow((layer_side - 2), 2) + 1

    target_offset = target - layer_start
    quarter_length = layer_side - 1
    target_quarter = int(target_offset / quarter_length)

    quarter_offset = target_offset - (target_quarter * quarter_length) + 1
    q_center_offset = math.fabs(quarter_offset - (quarter_length / 2))

    dist_to_center = layer_number + q_center_offset
    return dist_to_center


def coords_iter():
    x, y = 0, 0
    increment = (0, 1)
    increment_range = 1
    while True:
        for i in range(increment_range):
            yield (x, y)
            x += increment[0]
            y += increment[1]
        increment = increment[1], increment[0]

        for i in range(increment_range):
            yield (x, y)
            x += increment[0]
            y += increment[1]
        increment = -increment[1], -increment[0]

        increment_range += 1


def part_2(target):
    coords = coords_iter()
    neighbour_coords = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1), (0, 0), (0, 1),
        (1, -1), (1, 0), (1, 1),
    ]

    # Initialize grid to (0, 0): 1
    grid = {next(coords): 1}

    for coord in coords:
        value = 0
        for neighbour in neighbour_coords:
            value += grid.get((coord[0] + neighbour[0], coord[1] + neighbour[1]), 0)
        grid[coord] = value

        if value > 289326:
            print coord, value
            break


def main():
    print '#\tLayer\tSide\tStart/End\tWidth\tOffset\tQrt.\tQrt. Offset\tDist Ofst.\tCenter Dist.'

    for i in range(2, 52):
        layer_side = math.ceil(math.sqrt(i))
        if layer_side % 2 == 0:
            layer_side += 1
        layer_number = (layer_side - 1) / 2

        layer_start = math.pow((layer_side - 2), 2) + 1
        layer_end = layer_side * layer_side

        target_offset = i - layer_start
        layer_width = layer_end - layer_start + 1
        quarter_length = layer_side - 1
        target_quarter = int(target_offset / quarter_length)

        quarter_offset = target_offset - (target_quarter * quarter_length) + 1
        q_center_offset = math.fabs(quarter_offset - (quarter_length / 2))

        dist_to_center = layer_number + q_center_offset

        print '%d\t%d\t%d\t%d - %d\t\t%d\t%d\t%d\t%d\t\t%d\t\t%d' % (
            i, layer_number, layer_side, layer_start, layer_end, layer_width,
            target_offset, target_quarter, quarter_offset, q_center_offset,
            dist_to_center
        )


if __name__ == '__main__':
    print part_2(square_id)
