
import re
import sys

rule_1_re = re.compile(r'.*(abc|bcd|cde|def|efg|fgh|pqr|qrs|rst|stu|tuv|uvw|vwx|wxy|xyz).*')
rule_2_re = re.compile(r'^[^iol]+$')
rule_3_re = re.compile(r'.*((\w)\2)+.*((\w)\4)+.*')


def main(input_data):
    password = get_next_password(input_data)
    print 'Part 1:', ''.join(password)
    password = get_next_password(password)
    print 'Part 2:', ''.join(password)


def get_next_password(current_password):
    password = list(current_password)

    password = increment_password(password)
    while not meets_criteria(password):
        password = increment_password(password)

    return password


def meets_criteria(password):
    string_password = ''.join(password)
    return (
        rule_1_re.match(string_password) and
        rule_2_re.match(string_password) and
        rule_3_re.match(string_password)
    )


def increment_password(password):
    letter_index = len(password) - 1
    while True:
        letter = password[letter_index]
        if letter == 'z':  # Wrap around
            password[letter_index] = 'a'
            letter_index -= 1
        else:
            if letter in ['h', 'n', 'k']:   # Skip i, o, and l
                password[letter_index] = increment_letter(letter, incr=2)
            else:
                password[letter_index] = increment_letter(letter)
            return password


def increment_letter(letter, incr=1):
    return chr(ord(letter) + incr)

if __name__ == '__main__':
    main(sys.argv[1])
