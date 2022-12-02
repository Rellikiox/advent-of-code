import sys
import heapq


def main(input_filename: str):
    with open(input_filename, "r") as stream:
        data = stream.read().strip()

    print("Part 1:", part_1(data))
    print("Part 2:", part_2(data))


def part_1(data: str) -> int:
    return max(
        sum(int(value.strip()) for value in elf.split("\n"))
        for elf in data.split("\n\n")
    )


def part_2(data):
    return sum(
        heapq.nlargest(
            3,
            (
                sum(int(value.strip()) for value in elf.split("\n"))
                for elf in data.split("\n\n")
            ),
        )
    )


if __name__ == "__main__":
    main(sys.argv[1])
