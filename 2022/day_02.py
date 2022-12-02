import sys

# Shape points:
# Rock: 1, Paper: 2, Scissors: 3

# Result points:
# Lose: 0, Draw: 3, Win: 6

# A, B, C = P1 Rock, Paper, Scissors
# X, Y, Z = P2 Rock, Paper, Scissors
PART_1_POINTS = {
    "A X": 1 + 3,
    "A Y": 2 + 6,
    "A Z": 3 + 0,
    "B X": 1 + 0,
    "B Y": 2 + 3,
    "B Z": 3 + 6,
    "C X": 1 + 6,
    "C Y": 2 + 0,
    "C Z": 3 + 3,
}

# A, B, C = P1 Rock, Paper, Scissors
# X, Y, Z = P2 Lose, Draw, Win
PART_2_POINTS = {
    "A X": 3 + 0,
    "A Y": 1 + 3,
    "A Z": 2 + 6,
    "B X": 1 + 0,
    "B Y": 2 + 3,
    "B Z": 3 + 6,
    "C X": 2 + 0,
    "C Y": 3 + 3,
    "C Z": 1 + 6,
}


def main(input_filename):
    with open(input_filename) as stream:
        data = stream.read().strip()

    print("Part 1:", part_1(data))
    print("Part 2:", part_2(data))


def part_1(data):
    return sum(PART_1_POINTS[line.strip()] for line in data.split("\n"))


def part_2(data):
    return sum(PART_2_POINTS[line.strip()] for line in data.split("\n"))


if __name__ == "__main__":
    main(sys.argv[1])
