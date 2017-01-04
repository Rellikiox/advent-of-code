import string
import time


test_input = ['1', '0', '11111', '111100001010']


def rec_dragon_data(a, length):
    if len(a) >= length:
        return a[:length]

    return rec_dragon_data(
        a + '0' + a.replace('0', ' ').replace('1', '0').replace(' ', '1')[::-1],
        length
    )


def it_dragon_data(a, length):
    while len(a) < length:
        a += '0' + a.replace('0', ' ').replace('1', '0').replace(' ', '1')[::-1]

    return a[:length]


def it_dragon_data_translate(a, length):
    while len(a) < length:
        a += '0' + a.translate(string.maketrans("01", "10"))[::-1]

    return a[:length]


def it_dragon_data_loop(a, length):
    while len(a) < length:
        b = ''
        for i in range(len(a)):
            b += '0' if a[i] == '1' else '1'
        a += '0' + b[::-1]

    return a[:length]


def rec_get_checksum(data):
    checksum = ''.join([
        str(int(data[i] == data[i + 1]))
        for i in range(0, len(data), 2)
    ])

    if len(checksum) % 2 == 0:
        return rec_get_checksum(checksum)

    return checksum


def it_get_checksum(data):
    checksum = checksum = ''.join([
        str(int(data[i] == data[i + 1]))
        for i in range(0, len(data), 2)
    ])
    while len(checksum) % 2 == 0:
        checksum = ''.join([
            str(int(checksum[i] == checksum[i + 1]))
            for i in range(0, len(checksum), 2)
        ])

    return checksum


def rec_random_data(initial_state, length):
    return rec_get_checksum(rec_dragon_data(initial_state, length))


def it_random_data(initial_state, length):
    return it_get_checksum(it_dragon_data_translate(initial_state, length))


def main():
    t = time.time()
    print it_dragon_data('1', 100), time.time() - t
    t = time.time()
    print it_dragon_data_translate('1', 100), time.time() - t
    t = time.time()
    print it_dragon_data_loop('1', 100), time.time() - t


if __name__ == '__main__':
    main()
