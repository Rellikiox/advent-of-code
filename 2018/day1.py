
import sys


def circular_iter(list_to_iter):
    idx = 0
    while True:
        yield list_to_iter[idx]
        idx += 1
        if idx == len(list_to_iter):
            idx = 0


def main(input_file):
    with open(input_file) as stream:
        data = stream.read()

    print 'Part 1:', eval(data.replace('\n', ''))

    frequency = 0
    seen = set([0])
    for change in circular_iter(data.split('\n')):
        frequency += int(change)
        if frequency in seen:
            print 'Part 2:', frequency
            break
        else:
            seen.add(frequency)


if __name__ == '__main__':
    main(sys.argv[1])
