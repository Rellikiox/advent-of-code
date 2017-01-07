
from collections import namedtuple
import re


test_input = """root@ebhq-gridcenter# df -h
Filesystem              Size  Used  Avail  Use%
/dev/grid/node-x0-y0     30T   25T     5T   81%
/dev/grid/node-x0-y1     40T   12T    28T   77%
/dev/grid/node-x1-y0     35T    9T    26T   77%
/dev/grid/node-x1-y1     10T    1T     9T   73%"""

node_re = r'/dev/grid/node-x(\d+)-y(\d+)\s+\d+T\s+(\d+)T\s+(\d+)T\s+\d+%'
Node = namedtuple('Node', ['x', 'y', 'used', 'avail'])


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


def n_viable_pairs(input):
    node_list = parse_nodes(input)
    # print node_list
    return len(viable_pairs(node_list))


def main():
    node_list = parse_nodes(test_input)
    # print node_list
    print len(viable_pairs(node_list))


if __name__ == '__main__':
    main()
