import pprint
from collections import namedtuple
import re
import math


test_input = """root@ebhq-gridcenter# df -h
Filesystem              Size  Used  Avail  Use%
/dev/grid/node-x0-y0     30T   25T     5T   81%
/dev/grid/node-x0-y1     40T   12T    28T   77%
/dev/grid/node-x1-y0     35T    9T    26T   77%
/dev/grid/node-x1-y1     10T    1T     9T   73%"""

node_re = r'/dev/grid/node-x(\d+)-y(\d+)\s+\d+T\s+(\d+)T\s+(\d+)T\s+\d+%'
Node = namedtuple('Node', ['x', 'y', 'used', 'avail'])

test_input = """root@ebhq-gridcenter# df -h
Filesystem            Size  Used  Avail  Use%
/dev/grid/node-x0-y0   10T    8T     2T   80%
/dev/grid/node-x0-y1   11T    6T     5T   54%
/dev/grid/node-x0-y2   32T   28T     4T   87%
/dev/grid/node-x1-y0    9T    7T     2T   77%
/dev/grid/node-x1-y1    8T    0T     8T    0%
/dev/grid/node-x1-y2   11T    7T     4T   63%
/dev/grid/node-x2-y0   10T    6T     4T   60%
/dev/grid/node-x2-y1    9T    8T     1T   88%
/dev/grid/node-x2-y2    9T    6T     3T   66%"""


def parse_nodes(input):
    lines = input.split('\n')
    return [
        Node(*map(int, re.findall(node_re, l)[0]))
        for l in lines[2:]
        if l.strip()
    ]


def viable_pairs(nodes):
    by_used = sorted(nodes, key=lambda n: n.used)
    by_avail = sorted(nodes, key=lambda n: -n.avail)

    viable_pairs = []
    for used_n in by_used:
        added_any = False
        if used_n.used == 0:
            continue
        for avail_n in by_avail:
            if used_n.used <= avail_n.avail:
                if used_n != avail_n:
                    added_any = True
                    viable_pairs.append((used_n, avail_n))
            else:
                # Since the list are sorted, if used_n does't fit on avail_n it wont fit
                # on any of the others left on the avail list
                break
        if not added_any:
            # If this flag is not set it means this node did not create any viable pairs,
            # which means its used is more than any of the available nodes, and since nodes
            # after this one are even bigger they wont fit either, so we can safely exit
            break

    return viable_pairs


def print_map(nodes, can_be_emptied, can_be_filled):
    x_len = max(n.x for n in nodes)
    y_len = max(n.y for n in nodes)
    nodes_2d = [
        [None] * (x_len + 1)
        for i in range(y_len + 1)
    ]

    for n in nodes:
        nodes_2d[n.y][n.x] = n

    print '\n'.join([
        '\t'.join([
            '[{}/{}]'.format(node.used, node.used + node.avail)
            if node in can_be_emptied
            else '({}/{})'.format(node.used, node.used + node.avail)
            if node in can_be_filled
            else '{}/{}'.format(node.used, node.used + node.avail)
            for node in line
        ])
        for line in nodes_2d
    ])


def n_viable_pairs(input):
    node_list = parse_nodes(input)
    # print node_list
    return len(viable_pairs(node_list))


def main():
    node_list = parse_nodes(open('day22input.txt').read())
    pprint.pprint(viable_pairs(node_list))
    print_map(
        node_list,
        set(p[0] for p in viable_pairs(node_list)),
        set(p[1] for p in viable_pairs(node_list))
    )


if __name__ == '__main__':
    main()
