
import yaml
import os
import sys
import requests
from bs4 import BeautifulSoup


file_template = """
import sys


def main(input_filename):
    with open(input_filename) as stream:
        data = stream.read().strip()

    print 'Part 1:', None
    print 'Part 2:', None


if __name__ == '__main__':
    main(sys.argv[1])
"""
source_filename = 'day{}.py'
input_filename = 'input{}.txt'
config_file = 'config.yaml'
instructions_url = 'https://adventofcode.com/{}/day/{}'
input_url = instructions_url + '/input'


def main(year, day):

    if not os.path.isdir(year):
        os.mkdir(year)

    source_file_path = os.path.join(year, source_filename.format(day))
    if not os.path.isfile(source_file_path):
        with open(source_file_path, 'w') as stream:
            stream.write(file_template)

    input_file_path = os.path.join(year, input_filename.format(day))
    if not os.path.isfile(input_file_path):
        with open(config_file) as stream:
            cookies = yaml.load(stream)['cookies']

        response = requests.get(input_url.format(year, day), cookies=cookies)
        with open(input_file_path, 'w') as stream:
            stream.write(response.text)

    print instructions_url.format(year, day)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
