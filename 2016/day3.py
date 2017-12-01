
import re


test_input = """
1 2 2
1 2 4
2 2 1
2 4 1
2 1 2
4 1 2
"""

test_output = 3


def are_triangles(input):
    columns = [[], [], []]
    for line in input.split('\n'):
        if line:
            a, b, c = [int(s) for s in re.findall(r'\d+', line)]
            columns[0].append(a)
            columns[1].append(b)
            columns[2].append(c)
    single_column = columns[0] + columns[1] + columns[2]

    return [
        is_triangle_from_list(single_column[i:i + 3])
        for i in range(0, len(single_column), 3)
    ].count(True)


def is_triangle_from_list(numbers):
    try:
        a, b, c = sorted(numbers)
    except Exception as e:
        import pdb; pdb.set_trace()
        raise e
    return (a + b > c)


def is_triangle_from_string(line):
    a, b, c = sorted([int(s) for s in re.findall(r'\d+', line)])
    return (a + b > c)


def main():
    assert are_triangles(test_input) == test_output


if __name__ == '__main__':
    main()
