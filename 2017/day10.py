

def main():
    lengths = read_integer_lengths()
    data = range(256)
    sparse_hash = get_sparse_hash(lengths, data, rounds=1)
    print 'Part 1:', sparse_hash[0] * sparse_hash[1]

    lengths = read_ascii_lengths() + [17, 31, 73, 47, 23]
    data = range(256)
    sparse_hash = get_sparse_hash(lengths, data, rounds=64)
    print 'Part 2:', get_dense_hash(sparse_hash)


def get_sparse_hash(lengths, data, rounds):
    position = 0
    skip_size = 0
    for i in range(rounds):
        for length in lengths:
            sub_list = get_sublist(data, position, length)
            set_sublist(data, position, sub_list[::-1])
            position = (position + length + skip_size) % len(data)
            skip_size += 1

    return data


def get_dense_hash(data):
    dense_hash = []
    for idx in xrange(0, len(data), 16):
        xor = data[idx]
        for n in data[idx + 1:idx + 16]:
            xor ^= n
        dense_hash.append(xor)

    return ''.join(["{0:0{1}x}".format(item, 2) for item in dense_hash])


def read_integer_lengths():
    with open('day10.input') as day10:
        return [int(length) for length in day10.read().split(',')]


def read_ascii_lengths():
    with open('day10.input') as day10:
        return [ord(character) for character in day10.read().strip()]


def get_sublist(data, position, length):
    if position + length <= len(data):
        return data[position:position + length]
    else:
        return data[position:] + data[:position + length - len(data)]


def set_sublist(data, position, sub_list):
    if position + len(sub_list) <= len(data):
        data[position:position + len(sub_list)] = sub_list
    else:
        sub_list_break = len(data) - position
        data[position:] = sub_list[:sub_list_break]
        data[:len(sub_list) - sub_list_break] = sub_list[sub_list_break:]

    return data


if __name__ == '__main__':
    main()