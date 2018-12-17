
import sys


def main(input_file):
    with open(input_file) as stream:
        lines = [
            line.split(' ')
            for line in stream.read().split('\n')
        ]

    word_parts = []
    for words in zip(*lines):
        unique_words = list(set(words))
        word_parts.append(unique_words)

    regex_parts = []
    for word_list in word_parts:
        if len(word_list) == 1:
            regex_parts.append(word_list[0])
        else:
            regex_parts.append('([a-zA-Z0-9_]+)')

    regex = 'r\'{}\''.format(' '.join(regex_parts))
    print regex


if __name__ == '__main__':
    main(sys.argv[1])
