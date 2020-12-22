

def run(data):
    passwords = []
    for line in data.split('\n'):
        if not line:
            continue
        range_vals, letter, password = line.split(' ')
        range_vals = range_vals.split('-')
        passwords.append((int(range_vals[0]), int(range_vals[1]), letter[0], password))

    part1(passwords)
    part2(passwords)


def part1(passwords):
    valid = sum(
        int(min_n <= password.count(letter) <= max_n)
        for min_n, max_n, letter, password in passwords
    )
        
    print(f'Part 1: {valid}')


def part2(passwords):
    valid = sum(
        int((password[pos_a - 1] == letter) != (password[pos_b - 1] == letter))
        for pos_a, pos_b, letter, password in passwords
    )

    print(f'Part 2: {valid}')
