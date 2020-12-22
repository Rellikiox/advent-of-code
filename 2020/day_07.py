
import re

bag_name_re = re.compile(r'(\w+ \w+) bags?')
bag_amount_re = re.compile(r'(\d) (\w+ \w+) bags?')


def parse_data(data):
    rules = {}
    for row in data.split('\n'):
        if not row:
            continue

        name, contents = row.split(' contain ')
        name = bag_name_re.match(name).group(1)

        rules[name] = bag_amount_re.findall(contents)

    return rules


def explode_rule(color, rules):
    inner_colors = []
    for amount, other in rules[color]:
        inner_colors.append(other)
        inner_colors.extend(explode_rule(other, rules))
    return inner_colors


def part1(rules):
    print(f'Part 1: {sum("shiny gold" in explode_rule(color, rules) for color in rules)}')


def count_bags(color, rules):
    inner_bags = 0
    for amount, other in rules[color]:
        amount = int(amount)
        inner_bags += amount + amount * count_bags(other, rules)
    return inner_bags


def part2(rules):
    print(f'Part 2: {count_bags("shiny gold", rules)}')
