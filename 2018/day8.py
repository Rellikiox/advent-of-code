
import sys


class Node(object):
    def __init__(self, input_data, read_index):
        self.n_children = input_data[read_index]
        n_metadata = input_data[read_index + 1]

        self.children = []
        read_index += 2
        for _ in range(self.n_children):
            child = Node(input_data, read_index)
            self.children.append(child)
            read_index = child.end_index

        metadata_start = read_index
        self.end_index = metadata_start + n_metadata
        self.metadata = input_data[metadata_start:self.end_index]

    def metadata_checksum(self):
        my_metadata_checksum = sum(self.metadata)
        child_metadata = sum(child.metadata_checksum() for child in self.children)
        return my_metadata_checksum + child_metadata

    def value(self):
        if not self.children:
            return self.metadata_checksum()
        else:
            children_to_sum = [
                self.children[child_index - 1]
                for child_index in self.metadata
                if 0 <= child_index - 1 < self.n_children
            ]
            return sum(child.value() for child in children_to_sum)


def main(input_filename):
    with open(input_filename) as stream:
        root_node = Node([int(v) for v in stream.read().strip().split(' ')], 0)

    print 'Part 1:', root_node.metadata_checksum()
    print 'Part 2:', root_node.value()


if __name__ == '__main__':
    main(sys.argv[1])
