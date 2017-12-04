

def main():
    with open('day4.input') as passphrases:
        return count_valid_passphrases_no_anagrams(passphrases)


def count_valid_passphrases(stream):
    """For each line (stripped of whitespace) split it in words. If the list of words
    has the same lenght as the set of words (sets automatically remove unique items)
    then the passphrase is valid"""
    return sum(
        len(passphrase) == len(set(passphrase))
        for passphrase in [line.strip().split(' ') for line in stream]
    )


def count_valid_passphrases_no_anagrams(stream):
    """Same as the above, but before checking lengths we sort each individual word so
    that any possible anagrams are in the same order. This way we don't have to care about
    them being anagrams"""
    return sum(
        len(passphrase) == len(set(passphrase))
        for passphrase in (
            [''.join(sorted(word)) for word in passphrase]
            for passphrase in (
                line.strip().split(' ')
                for line in stream
            )
        )
    )


if __name__ == '__main__':
    print main()

    # test_input = ['aa bb cc dd ee', 'aa bb cc dd aa', 'aa bb cc dd aaa']

    # print count_valid_passphrases(test_input)
