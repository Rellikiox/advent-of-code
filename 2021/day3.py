import sys
from collections import Counter


def main(input_filename):
    with open(input_filename) as stream:
        data = [list(line.strip()) for line in stream.read().strip().split("\n")]

    print("Part 1:", part_1(data))
    print("Part 2:", part_2(data))


def part_1(data):
    gamma, epsilon = [], []
    for bit_array in zip(*data):
        most_common = Counter(bit_array).most_common()
        gamma.append(most_common[0][0][0])
        epsilon.append(most_common[-1][0][0])

    return int(''.join(gamma), 2) * int(''.join(epsilon), 2)


def part_2(data):
    o2_gen, co2_scrubber = 0, 0


if __name__ == "__main__":
    main(sys.argv[1])
