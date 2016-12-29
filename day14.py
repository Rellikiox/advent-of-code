
import hashlib

test_salt = 'abc'


def get_64_keys(salt):
    hashes = {}
    keys = []

    i = 0
    while len(keys) < 64:
        unhashed_key = salt + str(i)
        hashed_key, hashes = get_stretched_hash(unhashed_key, hashes)
        trip_char = get_trip(hashed_key)
        if trip_char:
            for j in range(1, 1001):
                other_unhashed_key = salt + str(i + j)
                other_hashed_key, hashes = get_stretched_hash(other_unhashed_key, hashes)
                if has_quint(other_hashed_key, trip_char):
                    keys.append(unhashed_key)
                    print 'found hash', unhashed_key
                    break
        i += 1

    return keys


def get_hash(unhashed_data, hashes):
    hashed_key = hashes.get(unhashed_data)
    if not hashed_key:
        hashed_key = hashlib.md5(unhashed_data).hexdigest().lower()
        hashes[unhashed_data] = hashed_key
    return hashed_key, hashes


def get_stretched_hash(unhashed_data, hashes):
    hashed_key = hashes.get(unhashed_data)
    if not hashed_key:
        hashed_key = unhashed_data
        for i in range(2017):
            hashed_key = hashlib.md5(hashed_key).hexdigest().lower()
    hashes[unhashed_data] = hashed_key
    return hashed_key, hashes


def get_trip(key):
    for i in range(len(key) - 2):
        if key[i] == key[i + 1] == key[i + 2]:
            return key[i]
    return None


def has_quint(key, char):
    for i in range(len(key) - 4):
        if char == key[i] == key[i + 1] == key[i + 2] == key[i + 3] == key[i + 4]:
            return True
    return False


def main():
    print get_64_keys(test_salt)


if __name__ == '__main__':
    main()
