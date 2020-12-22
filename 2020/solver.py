
import requests
import sys
import os
import importlib


source_file_template = '''

def parse_data(data):
    return data


def part1(data):
    print(f'Part 1: {0}')


def part2(data):
    print(f'Part 2: {0}')
'''


def download():
    day = int(sys.argv[2])
    download_url = f'https://adventofcode.com/2020/day/{day}/input'
    instructions_url = f'https://adventofcode.com/2020/day/{day}'
    input_filename = f'day_{day:02d}.txt'
    test_input_filename = f'day_{day:02d}.test.txt'
    source_filename = f'day_{day:02d}.py'
    
    print(f'Setting up day #{day}:')

    if not os.path.isfile(source_filename):
        with open(source_filename, 'w') as stream:
            stream.write(source_file_template)
        print(f'\t> Created {source_filename}')
    else:
        print(f'\t> {source_filename} already exists, skipping creation')

    if not os.path.isfile(input_filename):
        cookies = {
            'session': '53616c7465645f5fb405a110350cd0da50c2971545e43a9ef6f72d3c0acf376a'
        }
        response = requests.get(download_url, cookies=cookies)
        if response.status_code == 200:
            with open(input_filename, 'wb') as stream:
                stream.write(response.content)
            print(f'\t> Downloaded input file to {input_filename}')
        else:
            print('\t> No input data found')
    else:
        print(f'\t> {input_filename} already exists, skipping download')

    if not os.path.isfile(test_input_filename):
        with open(test_input_filename, 'w') as stream:
            pass
        print(f'\t> Created empty test input file {test_input_filename}')
    else:
        print(f'\t> {test_input_filename} already exists, skipping creation')

        

    print(f'\t> Instructions at {instructions_url}')


def run(test_mode=False):
    day = int(sys.argv[2])
    source_filename = f'day_{day:02d}'
    module = importlib.import_module(source_filename)

    input_filename = f'day_{day:02d}.txt' if not test_mode else f'day_{day:02d}.test.txt'
    if os.path.isfile(input_filename):
        with open(input_filename, 'r') as stream:
            data = module.parse_data(stream.read())
    else:
        data = None

    if test_mode and hasattr(module, 'test'):
        module.test(data)
    else:
        module.part1(data)
        module.part2(data)


if __name__ == '__main__':
    if sys.argv[1] == 'download':
        download()
    elif sys.argv[1] == 'run':
        run()
    elif sys.argv[1] == 'test':
        run(test_mode=True)