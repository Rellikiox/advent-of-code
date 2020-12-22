

def parse_data(data):
    return [
        [answers for answers in group.split('\n') if answers]
        for group in data.split('\n\n')
        if group
    ]


def part1(data):
    total_uniques = 0
    for group in data:
        unique_answers = set()
        for person in group:
            for char in person:
                unique_answers.add(char)
        total_uniques += len(unique_answers)
    print(f'Part 1: {total_uniques}')


def part2(data):
    total_uniques = 0
    for group in data:
        unique_answers = {}
        for person in group:
            for char in person:
                unique_answers[char] = unique_answers.get(char, 0) + 1

        for n_answer in unique_answers.values():
            total_uniques += len(group) == n_answer

    print(f'Part 2: {total_uniques}')
