
import hashlib


test_input = 'abc'
test_ouput = '18f47a30'


def get_password(input):
    password = ''

    idx = 0
    while len(password) < 8:
        next_hash = hashlib.md5('{}{}'.format(input, idx)).hexdigest()
        if next_hash.startswith('00000'):
            password += next_hash[5]

        if idx % 100000 == 0:
            print idx, password

        idx += 1

    return password


def get_password_with_order(input):
    password = ['_'] * 8

    idx = 0
    while '_' in password:
        next_hash = hashlib.md5('{}{}'.format(input, idx)).hexdigest()
        if next_hash.startswith('00000') and '0' <= next_hash[5] <= '7':
            next_char = next_hash[6]
            next_char_idx = next_hash[5]
            if password[int(next_char_idx)] == '_':
                password[int(next_char_idx)] = next_char

        if idx % 1000000 == 0:
            print idx, ''.join(password)

        idx += 1

    return ''.join(password)


def main():
    print get_password(test_input), test_ouput


if __name__ == '__main__':
    main()
