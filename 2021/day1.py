
import sys


def main(input_filename):
    with open(input_filename) as stream:
        data = [
            int(line) for line in 
            stream.read().strip().split('\n')
        ]

    print('Part 1:', part_1(data))
    print('Part 2:', part_2(data))


def part_1(data):
    prev_line = None
    increases = 0
    for line in data:
        if prev_line is not None and prev_line < line:
            increases += 1
        prev_line = line
    return increases


def part_2(data):
    prev_measure = None
    increases = 0
    for idx in range(len(data) - 2):
        current_measure = sum(data[idx:idx+3])
        if prev_measure is not None and prev_measure < current_measure:
            increases += 1
        prev_measure = current_measure
    return increases


if __name__ == '__main__':
    main(sys.argv[1])


