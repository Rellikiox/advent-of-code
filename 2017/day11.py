
import math


def main():
    with open('day11.input') as day11:
        movements = day11.read().split(',')
        diag_one_moves = math.fabs(movements.count('ne') - movements.count('sw'))
        diag_two_moves = math.fabs(movements.count('nw') - movements.count('se'))
        vertical_moves = math.fabs(movements.count('n') - movements.count('s'))

        print 'Part 1:', diag_one_moves + diag_two_moves + vertical_moves


if __name__ == '__main__':
    main()