
import math


def parse_data(data):
    trees = []
    for idx, line in enumerate(data.split('\n')):
        if not line:
            continue
        trees.append([])
        for char in line:
            trees[idx].append(char == '#')
    return trees


def count_slope(trees, slope):
    position = (0, 0)
    tree_hits = 0
    width = len(trees[0])
    height = len(trees)
    while position[1] < height:
        x, y = position
        tree_hits += int(trees[y][x])
        position = (
            (x + slope[0]) % width, 
            (y + slope[1])
        )
    return tree_hits


def part1(trees):
    print(f'Part 1: {count_slope(trees, (3, 1))}')


def part2(trees):
    slopes = [
        (1, 1),
        (3, 1),
        (5, 1),
        (7, 1),
        (1, 2)
    ]
    print(f'Part 2: {math.prod(count_slope(trees, slope) for slope in slopes)}')