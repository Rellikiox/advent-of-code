
def run(data):
    numbers = [int(line) for line in data.split('\n') if line]

    part1(numbers)
    part2(numbers)


def part1(numbers):
    target = 2020

    seen = set()
    for number in numbers:
        complement = 2020 - number
        if complement in seen:
            print(f'Part 01: {number * complement}')
            break
        seen.add(number)


def part2(numbers):
    numbers = sorted(numbers)
    
    i = 0
    j = 1
    k = 2

    loops = 0
    while True:
        loops += 1
        number_sum = numbers[i] + numbers[j] + numbers[k]
        if number_sum == 2020:
            print(f'Part 02: {numbers[i] * numbers[j] * numbers[k]} (in {loops} loops)')
            break
        
        k += 1            
        if k >= len(numbers) or number_sum > 2020:
            j += 1
            k = j + 1

        if j >= len(numbers) - 1:
            i += 1
            j = i + 1
            k = j + 1

        if i >= len(numbers) - 2:
            break
