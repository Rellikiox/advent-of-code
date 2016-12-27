
import re

test_data = [
    ('ADVENT', 'ADVENT'),
    ('A(1x5)BC', 'ABBBBBC'),
    ('(3x3)XYZ', 'XYZXYZXYZ'),
    ('A(2x2)BCD(2x2)EFG', 'ABCBCDEFEFG'),
    ('(6x1)(1x3)A', '(1x3)A'),
    ('X(8x2)(3x3)ABCY', 'X(3x3)ABC(3x3)ABCY')
]

test_data_expanding = [
    ('(3x3)XYZ', 9),
    ('(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN', 445),
    ('(27x12)(20x12)(13x14)(7x10)(1x12)A', 241920),
    ('X(8x2)(3x3)ABCY', 20)
]


def decompress(input):
    input = input.strip()
    result = ''

    idx = 0
    while idx < len(input):
        next_char = input[idx]
        if next_char == '(':
            marker = re.match(r'\((\d+)x(\d+)\)', input[idx:])
            length = int(marker.group(1))
            times = int(marker.group(2))

            # Advance index to end of marker
            idx += len(marker.group(0))

            result += input[idx:idx + length] * times
            idx += length
        else:
            result += next_char
            idx += 1

    return result


def decompress_expanding(input):
    input = input.strip()
    output_length = 0

    idx = 0
    while idx < len(input):
        next_char = input[idx]
        if next_char == '(' and re.match(r'\((\d+)x(\d+)\)', input[idx:]):
            marker = re.match(r'\((\d+)x(\d+)\)', input[idx:])
            length = int(marker.group(1))
            times = int(marker.group(2))

            marker_desc_length = len(marker.group(0))
            sub_marker_start = idx + marker_desc_length
            sub_marker_end = sub_marker_start + length

            exp_marker_length = decompress_expanding(input[sub_marker_start:sub_marker_end])
            output_length += exp_marker_length * times
            idx += length + marker_desc_length
        else:
            output_length += 1
            idx += 1

    return output_length


def main():
    for line in test_data_expanding:
        print line[0], decompress_expanding(line[0]), line[1]


if __name__ == '__main__':
    main()
