
import re


test_password = 'abcde'
test_instructions = """swap position 4 with position 0
swap letter d with letter b
reverse positions 0 through 4
rotate left 1 steps
move position 1 to position 4
move position 3 to position 0
rotate based on position of letter b
rotate based on position of letter d"""
test_output = 'decab'


re_swap_pos = r'swap position (\d+) with position (\d+)'
re_swap_letter = r'swap letter (\w+) with letter (\w+)'
re_rot_left = r'rotate left (\d+) steps?'
re_rot_right = r'rotate right (\d+) steps?'
re_rot_letter = r'rotate based on position of letter (\w+)'
re_reverse = r'reverse positions (\d+) through (\d+)'
re_move = r'move position (\d+) to position (\d+)'


def swap_pos(password, pos1, pos2):
    password[pos1], password[pos2] = password[pos2], password[pos1]
    return password


def swap_letter(password, letter1, letter2):
    return swap_pos(password, password.index(letter1), password.index(letter2))


def rot_left(password, rot):
    return password[rot:] + password[:rot]


def rot_right(password, rot):
    return password[-rot:] + password[:-rot]


def rot_letter(password, letter):
    """
    pos     rot     new pos
    0       1       1
    1       2       3
    2       3       5
    3       4       7
    4       6       2
    5       7       4
    6       8       6
    7       9       0
    """
    index = password.index(letter)
    return rot_right(password, (index + (1 if index < 4 else 2)) % len(password))


def un_rot_letter(password, letter):
    index = password.index(letter)
    if index == 0:
        return rot_left(password, 9 % len(password))
    if index % 2 == 0:
        return rot_left(password, ((index / 2) + 5) % len(password))
    return rot_left(password, ((index / 2) + 1) % len(password))


def reverse(password, start, end):
    return password[:start] + password[start:end + 1][::-1] + password[end + 1:]


def move(password, pos1, pos2):
    letter = password.pop(pos1)
    password.insert(pos2, letter)
    return password


def scrambled_password(password, instructions):
    password = [l for l in password]

    for inst in instructions.split('\n'):
        inst = inst.strip()
        if not inst:
            continue
        print '-', ''.join(password)
        print inst
        match = re.match(re_swap_pos, inst)
        if match:
            password = swap_pos(password, int(match.group(1)), int(match.group(2)))
            continue

        match = re.match(re_swap_letter, inst)
        if match:
            password = swap_letter(password, match.group(1), match.group(2))
            continue

        match = re.match(re_rot_left, inst)
        if match:
            password = rot_left(password, int(match.group(1)))
            continue

        match = re.match(re_rot_right, inst)
        if match:
            password = rot_right(password, int(match.group(1)))
            continue

        match = re.match(re_rot_letter, inst)
        if match:
            password = rot_letter(password, match.group(1))
            continue

        match = re.match(re_reverse, inst)
        if match:
            password = reverse(password, int(match.group(1)), int(match.group(2)))
            continue

        match = re.match(re_move, inst)
        if match:
            password = move(password, int(match.group(1)), int(match.group(2)))
            continue

        print inst

    return ''.join(password)


def unscrambled_password(password, instructions):
    password = [l for l in password]

    for inst in instructions.split('\n')[::-1]:
        inst = inst.strip()
        if not inst:
            continue
        print '-', ''.join(password)
        print inst
        match = re.match(re_swap_pos, inst)
        if match:
            password = swap_pos(password, int(match.group(1)), int(match.group(2)))
            continue

        match = re.match(re_swap_letter, inst)
        if match:
            password = swap_letter(password, match.group(1), match.group(2))
            continue

        match = re.match(re_rot_left, inst)
        if match:
            password = rot_right(password, int(match.group(1)))
            continue

        match = re.match(re_rot_right, inst)
        if match:
            password = rot_left(password, int(match.group(1)))
            continue

        match = re.match(re_rot_letter, inst)
        if match:
            password = un_rot_letter(password, match.group(1))
            continue

        match = re.match(re_reverse, inst)
        if match:
            password = reverse(password, int(match.group(1)), int(match.group(2)))
            continue

        match = re.match(re_move, inst)
        if match:
            password = move(password, int(match.group(2)), int(match.group(1)))
            continue

        raise Exception()

    return ''.join(password)


def main():
    print scrambled_password(test_password, test_instructions), test_output


if __name__ == '__main__':
    main()
