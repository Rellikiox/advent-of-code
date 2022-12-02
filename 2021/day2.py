
import sys


def main(input_filename):
    with open(input_filename) as stream:
        data = stream.read().strip().split('\n')

    print('Part 1:', part_1(data))
    print('Part 2:', part_2(data))


def part_1(data):
    horizontal, depth = 0, 0
    for line in data:
        match line.split():
            case ['forward', value]:
                horizontal += int(value)
            case ['down', value]:
                depth += int(value)
            case ['up', value]:
                depth -= int(value)
    return horizontal * depth


def part_2(data):
    horizontal, depth, aim = 0, 0, 0
    for line in data:
        match line.split():
            case ['forward', value]:
                horizontal += int(value)
                depth += aim * int(value)
            case ['down', value]:
                aim += int(value)
            case ['up', value]:
                aim -= int(value)
    return horizontal * depth


if __name__ == '__main__':
    main(sys.argv[1])


