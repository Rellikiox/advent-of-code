

def plus_one(index_increment):
    return index_increment + 1


def plus_one_minus_one(index_increment):
    return index_increment + 1 if index_increment < 3 else index_increment - 1


def calculate_jumps(increment_fn=plus_one):
    """We transform the input into a list and iterate over it. On each pass we take our current
    index, calculate the next increment with our increment_fn, add that ammount to our current
    index and add one to the number of steps made. Once our index gets out of bouds (i.e. our
    program exists its jump loop of hell) it'll trigger a IndexError, which we catch and then
    return the number of jumps made"""

    with open('day5.input') as input_f:
        jump_list = [int(line.strip()) for line in input_f]

    index = 0
    jumps_made = 0
    while True:
        try:
            index_increment = jump_list[index]
            jump_list[index] = increment_fn(index_increment)
            index += index_increment

            jumps_made += 1
        except IndexError:
            break

    return jumps_made


if __name__ == '__main__':
    # Part one
    print calculate_jumps(plus_one)

    # Part two
    print calculate_jumps(plus_one_minus_one)
