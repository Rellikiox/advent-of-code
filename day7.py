
import re

test_input = """abba[mnop]qrst
abcd[bddb]xyyx
aaaa[qwer]tyui
ioxxoj[asdfgh]zxcvbn"""

test_output = 2

ssl_test = """aba[bab]xyz
xyx[xyx]xyx
aaa[kek]eke
zazbz[bzb]cdb"""


def count_supports_tsl(input):
    return [supports_tsl(line) for line in input.split('\n')].count(True)


def supports_tsl(ip):
    inside_brackets = re.findall(r'\[(\w+)', ip)
    outside_brackets = [match[1] for match in re.findall(r'(^|\])([a-z]+)', ip)]
    return (
        (not any(has_abba(part) for part in inside_brackets)) and
        any(has_abba(part) for part in outside_brackets)
    )


def has_abba(line):
    return any(
        line[idx] != line[idx + 1] and
        line[idx] == line[idx + 3] and line[idx + 1] == line[idx + 2]
        for idx, s in enumerate(line[:-3])
    )


def count_supports_ssl(input):
    return [supports_ssl(line) for line in input.split('\n') if line.strip()].count(True)


def supports_ssl(ip):
    hypernets = re.findall(r'\[(\w+)', ip)

    supernets = [match[1] for match in re.findall(r'(^|\])([a-z]+)', ip)]
    for supernet in supernets:
        for aba in get_abas(supernet):
            for hypernet in hypernets:
                if aba_to_bab(aba) in hypernet:
                    return True

    return False


def get_abas(line):
    return [
        line[idx:idx + 3]
        for idx, s in enumerate(line[:-2])
        if (line[idx] != line[idx + 1] and line[idx] == line[idx + 2])
    ]


def aba_to_bab(aba):
    return aba[1] + aba[0] + aba[1]


def main():
    for line in test_input.split('\n'):
        print supports_tsl(line)


if __name__ == '__main__':
    main()
