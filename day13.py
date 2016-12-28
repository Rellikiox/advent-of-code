
class Point(object):
    def __init__(self, x, y, steps=0):
        self.x = x
        self.y = y
        self.steps = steps

    def equal_to(self, _other):
        return (self.x, self.y) == (_other.x, _other.y)

    def hash(self):
        return '{}.{}'.format(self.x, self.y)


def find_shortest(seed, goal):
    visited = set()
    frontier = [Point(1, 1, 0)]

    while frontier:
        current = frontier.pop(0)
        if current.hash() in visited:
            continue
        if current.equal_to(goal):
            return current.steps

        frontier.extend([
            p for p in get_next_points(current)
            if is_open(p, seed) and p.hash() not in visited
        ])
        visited.add(current.hash())
        print len(visited), '\t', len(frontier)

    return -1


def find_n_locations(seed, goal):
    visited = set()
    frontier = [Point(1, 1, 0)]

    while frontier:
        current = frontier.pop(0)
        if current.hash() in visited:
            continue

        frontier.extend([
            p for p in get_next_points(current)
            if is_open(p, seed) and p.hash() not in visited and p.steps <= goal
        ])
        visited.add(current.hash())
        print len(visited), '\t', len(frontier)

    return len(visited)


def get_next_points(p):
    points = []
    if p.x > 0:
        points.append(Point(p.x - 1, p.y, p.steps + 1))
    if p.y > 0:
        points.append(Point(p.x, p.y - 1, p.steps + 1))

    points.append(Point(p.x + 1, p.y, p.steps + 1))
    points.append(Point(p.x, p.y + 1, p.steps + 1))
    return points


def is_open(p, seed):
    base_10 = seed + p.x * p.x + 3 * p.x + 2 * p.x * p.y + p.y + p.y * p.y
    return n_of_1_bits(base_10) % 2 == 0


def n_of_1_bits(n):
    c = 0
    while n:
        c += 1
        n &= n - 1
    return c


def main():
    print find_shortest(1352, Point(31, 39))
    print find_n_locations(1352, 50)


if __name__ == '__main__':
    main()
