from collections import namedtuple

test_input = """5-8
0-2
4-7
1-5"""

IPRange = namedtuple('IPRange', ['min', 'max'])


def needs_merging(r1, r2):
    return r1.min <= r2.min <= r1.max or r1.min <= r2.max <= r1.max


def lowest_allowed_ip(test_input):
    ranges = sorted(
        (
            IPRange(*map(int, line.strip().split('-')))
            for line in test_input.split('\n') if line.strip()
        ),
        key=lambda r: r.min
    )

    """
    Now we have all the ranges sorted by their starting point.
    Starting at 0 we have to find the first allowed ip.

    we take 0 as our assumption of a free ip, and iterating over the
    ranges we do the following:
        - if min > assumption then return assumption
        - if min <= assumption <= max then assumption = max + 1
        - to get the next range to compare:
            - if next.max <= curr.max then next = next.next

    """

    assumption = 0
    idx = 0
    while idx < len(ranges):
        curr = ranges[idx]
        if curr.min > assumption:
            return assumption
        assumption = curr.max + 1

        idx += 1
        try:
            while ranges[idx].max <= curr.max:
                idx += 1
        except:
            break

    return None


def n_allowed_ip(test_input):
    ranges = sorted(
        (
            IPRange(*map(int, line.strip().split('-')))
            for line in test_input.split('\n') if line.strip()
        ),
        key=lambda r: r.min
    )

    """
    Now we have all the ranges sorted by their starting point.
    Starting at 0 we have to find the first allowed ip.

    we take 0 as our assumption of a free ip, and iterating over the
    ranges we do the following:
        - if min > assumption then return assumption
        - if min <= assumption <= max then assumption = max + 1
        - to get the next range to compare:
            - if next.max <= curr.max then next = next.next

    """

    assumption = 0
    total = 0
    idx = 0
    while idx < len(ranges):
        curr = ranges[idx]
        if curr.min > assumption:
            total += 1
            assumption += 1
        else:
            assumption = curr.max + 1

            idx += 1
            try:
                while ranges[idx].max <= curr.max:
                    idx += 1
            except:
                break

    return total


def main():
    print lowest_allowed_ip(test_input)


if __name__ == '__main__':
    main()
