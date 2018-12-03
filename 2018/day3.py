from itertools import product
import sys
import re

claim_re = r'#(\d+) @ (\d+),(\d+): (\d+)x(\d+)'


def get_inches(fabric, coord_list):
    return [
        fabric.setdefault(coord, [])
        for coord in coord_list
    ]


def is_claim_clear(claim_inches):
    return all(len(claims_in_inch) == 1 for claims_in_inch in claim_inches)


def main(input_file):
    with open(input_file) as stream:
        claims = stream.read().split('\n')

    fabric = {}
    claim_lookup = {}
    for claim in claims:
        claim_id, x, y, w, h = [int(value) for value in re.match(claim_re, claim).groups()]
        claim_coords = product(range(x, x + w), range(y, y + h))
        claim_inches = get_inches(fabric, claim_coords)
        for inch in claim_inches:
            inch.append(claim_id)
        claim_lookup[claim_id] = claim_inches

    print 'Part 1:', sum(len(fabric_claims) > 1 for fabric_claims in fabric.values())

    for claim_id, claim_inches in claim_lookup.iteritems():
        if is_claim_clear(claim_inches):
            print 'Part 2:', claim_id
            break


if __name__ == '__main__':
    main(sys.argv[1])
