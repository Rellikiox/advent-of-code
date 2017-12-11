
import re


def read_stream():
    with open('day9.input') as day9:
        return day9.read()


def clean_garbage(stream):
    stream = re.sub(r'!.', '', stream)
    sans_cancelled_len = len(stream)
    n_of_garbage = len(re.findall(r'<[^>]*>', stream))
    stream = re.sub(r'<[^>]*>', '', stream)
    sans_garbage_len = len(stream)
    return stream, (sans_cancelled_len - sans_garbage_len - n_of_garbage * 2)


def calc_group_score(stream):
    current_level = 0
    total_score = 0

    for char in stream:
        if char == '{':
            current_level += 1
        elif char == '}':
            total_score += current_level
            current_level -= 1

    return total_score


def main():
    stream = read_stream()
    stream, character_count = clean_garbage(stream)
    group_score = calc_group_score(stream)
    print group_score, character_count


def test_data():
    test_input = [
        ('<>', 0),
        ('<random characters>', 17),
        ('<<<<>', 3),
        ('<{!>}>', 2),
        ('<!!>', 0),
        ('<!!!>>', 0),
        ('<{o"i!a,<{i<a>', 10)
    ]

    for line in test_input:
        print clean_garbage(line[0]), line[1]


if __name__ == '__main__':
    main()
