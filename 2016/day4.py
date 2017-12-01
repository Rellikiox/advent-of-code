
import re


test_input = """aaaaa-bbb-z-y-x-123[abxyz]
a-b-c-d-e-f-g-h-987[abcde]
not-a-real-room-404[oarel]
totally-real-room-200[decoy]"""

test_output = 1514


def sum_real_rooms(input):
    return sum([
        get_room_id(l.strip())
        for l in input.split('\n')
        if l.strip() and is_real_room(l.strip())
    ])


def get_room_id(line):
    return int(re.findall(r'\d+', line)[0])


def is_real_room(line):
    # Get our letters
    letters = re.findall(r'[a-z]', line[:-7])

    # Count each letter
    letter_count = {
        letter: letters.count(letter) for letter in letters
    }

    # Get for each count which letters appear that many times
    reverse_letter_count = {}
    for letter, count in letter_count.iteritems():
        reverse_letter_count.setdefault(count, []).append(letter)

    # Get a list of the letters sorted by count
    sorted_letters = []
    for count_key in reversed(sorted(reverse_letter_count.keys())):
        sorted_letters.extend(sorted(reverse_letter_count[count_key]))

    # Check if the 5 most popular ones equal the checksum
    checksum = line[-6:-1]
    return checksum == ''.join(sorted_letters[:5])


def decrypt_room(line):
    room_id_number_match = re.match(r'([\w-]+)-(\d+)\[\w+\]', line)
    room_id = room_id_number_match.group(1).replace('-', ' ')
    number = int(room_id_number_match.group(2))
    rotation = number % 26

    new_room_id = ''
    for letter in room_id:
        new_room_id += rotate_letter(letter, rotation) if letter != ' ' else ' '

    return new_room_id, number


def rotate_letter(letter, rot):
    return chr(((ord(letter) - 97 + (rot % 26)) % 26) + 97)


def find_secret_room(input):
    for line in input.split('\n'):
        line = line.strip()
        if line:
            name, id = decrypt_room(line)
            if 'north' in name:
                print name, id


def main():
    print [get_room_id(line) for line in test_input.split('\n')]
    print sum_real_rooms(test_input), test_output


if __name__ == '__main__':
    main()
