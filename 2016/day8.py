
import re


test_input = """rect 3x2
rotate column x=1 by 1
rotate row y=0 by 4
rotate column x=1 by 1"""

test_output = """.#..#.#
#.#....
.#....."""


def get_off_screen(x=50, y=6):
    return [['.'] * x for i in range(y)]


def print_screen(screen):
    for row in screen:
        print ''.join(row)


def run(input, screen):
    print_screen(screen)
    for line in input.split('\n'):
        line = line.strip()
        if not line:
            continue

        if 'rect' in line:
            screen = draw_rect(line, screen)
        elif 'rotate column' in line:
            screen = rot_col(line, screen)
        elif 'rotate row' in line:
            screen = rot_row(line, screen)
        print '------------'
        print line
        print_screen(screen)

    return screen


def draw_rect(line, screen):
    x, y = [int(s) for s in re.findall(r'rect (\d+)x(\d+)', line)[0]]

    for i in range(x):
        for j in range(y):
            screen[j][i] = '#'

    return screen


def rot_col(line, screen):
    col, rot = [int(s) for s in re.findall(r'rotate column x=(\d+) by (\d+)', line)[0]]

    new_col = []
    col_length = len(screen)
    for i in range(col_length):
        new_col.append(screen[(i - rot) % col_length][col])

    for i in range(col_length):
        screen[i][col] = new_col[i]

    return screen


def rot_row(line, screen):
    row, rot = [int(s) for s in re.findall(r'rotate row y=(\d+) by (\d+)', line)[0]]

    for i in range(rot):
        screen[row].insert(0, screen[row].pop())

    return screen


def main():
    screen = get_off_screen(7, 3)
    screen = run(test_input, screen)
    print_screen(screen)


if __name__ == '__main__':
    main()
