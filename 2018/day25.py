
import sys
import math


def distance(star_a, star_b):
    return sum(math.fabs(a - b) for a, b in zip(star_a, star_b))


def main(input_filename):
    with open(input_filename) as stream:
        stars = sorted([
            tuple(int(v) for v in line.split(','))
            for line in stream.read().strip().split('\n')
        ])
    constelations = {
        star: tuple([star])
        for star in stars
    }

    for star_a in stars:
        for star_b in stars:
            if star_a is star_b:
                continue

            constelation_a = constelations[star_a]
            constelation_b = constelations[star_b]

            if star_a in constelation_b or star_b in constelation_a:
                continue

            if distance(star_a, star_b) <= 3:
                new_constelation = tuple(sorted(constelation_a + constelation_b))
                for star in new_constelation:
                    constelations[star] = new_constelation

    unique_constelations = set(constelations.values())
    print unique_constelations
    print 'Part 1:', len(unique_constelations)
    print 'Part 2:', None


if __name__ == '__main__':
    main(sys.argv[1])
