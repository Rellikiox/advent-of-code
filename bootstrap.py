import tomllib
import os
import sys
import requests


file_template = """
import sys


def main(input_filename):
    with open(input_filename) as stream:
        data = stream.read().strip()

    print('Part 1:', part_1(data))
    print('Part 2:', part_2(data))


def part_1(data):
    pass


def part_2(data):
    pass


if __name__ == '__main__':
    main(sys.argv[1])

"""


def main(year: int, day: int):

    instructions_url = f"https://adventofcode.com/{year}/day/{day}"
    input_url = instructions_url + "/input"

    year_directory = str(year)
    if not os.path.isdir(year_directory):
        os.mkdir(year_directory)

    source_file_path = os.path.join(year_directory, f"day_{day:02}.py")
    if not os.path.isfile(source_file_path):
        with open(source_file_path, "w") as stream:
            stream.write(file_template)

    with open("config.toml", "rb") as stream:
        config = tomllib.load(stream)

    input_file_path = os.path.join(year_directory, f"day_{day:02}_input.txt")
    if not os.path.isfile(input_file_path):

        response = requests.get(
            input_url.format(year, day),
            cookies=config["cookies"],
            headers=config["headers"],
        )
        with open(input_file_path, "w") as stream:
            stream.write(response.text)

    instructions_file_path = os.path.join(
        year_directory, f"day_{day:02}_instructions.txt"
    )
    response = requests.get(
        instructions_url,
        cookies=config["cookies"],
        headers=config["headers"],
    )
    with open(instructions_file_path, "w") as stream:
        stream.write(response.text)

    print(instructions_url)

    os.system(f"lynx {instructions_url} -dump")


if __name__ == "__main__":
    main(int(sys.argv[1]), int(sys.argv[2]))
