
import sys
import json


def main(input_file):
    with open(input_file) as stream:
        data = json.load(stream)

    print 'Part 1:', sum_items(data)


def sum_items(data):
    total_sum = 0
    for item in data:
        if isinstance(item, dict):
            if 'red' not in item.values() and 'red' not in item.keys():
                total_sum += sum_items(item.values())
        elif isinstance(item, list):
            total_sum += sum_items(item)
        elif isinstance(item, int):
            total_sum += item
    return total_sum


if __name__ == '__main__':
    main(sys.argv[1])
