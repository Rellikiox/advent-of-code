
test_input = """eedadn
drvtee
eandsr
raavrd
atevrs
tsrnev
sdttsa
rasrtv
nssdts
ntnada
svetve
tesnvt
vntsnd
vrdear
dvrsen
enarar"""

test_output = "easter"


def correct_most_common(input):
    columns = [[], [], [], [], [], [], [], []]
    for line in input.split('\n'):
        line = line.strip()
        for idx, s in enumerate(line):
            columns[idx].append(s)

    message = ['_'] * 8
    for idx, column in enumerate(columns):
        # Count each letter
        letter_count = {
            letter: column.count(letter) for letter in column
        }

        # Get for each count which letters appear that many times
        reverse_letter_count = {}
        for letter, count in letter_count.iteritems():
            reverse_letter_count.setdefault(count, []).append(letter)

        # Get the most frequent
        message[idx] = sorted(reverse_letter_count[sorted(reverse_letter_count.keys())[-1]])[0]

    return ''.join(message)


def correct_least_common(input):
    columns = [[], [], [], [], [], [], [], []]
    for line in input.split('\n'):
        line = line.strip()
        for idx, s in enumerate(line):
            columns[idx].append(s)

    message = ['_'] * 8
    for idx, column in enumerate(columns):
        # Count each letter
        letter_count = {
            letter: column.count(letter) for letter in column
        }

        # Get for each count which letters appear that many times
        reverse_letter_count = {}
        for letter, count in letter_count.iteritems():
            reverse_letter_count.setdefault(count, []).append(letter)

        # Get the most frequent
        message[idx] = sorted(reverse_letter_count[sorted(reverse_letter_count.keys())[0]])[0]

    return ''.join(message)


def main():
    print correct(test_input), test_output


if __name__ == '__main__':
    main()
