
import re


def parse_data(data):
    passports = [
        {
            field_pair.split(':')[0]: field_pair.split(':')[1]
            for field_pair in re.split(r'\n| ', passport) 
            if field_pair
        }
        for passport in data.split('\n\n')
    ]

    return passports


part_1_required_fields = [
    'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'
]

def part1(passports):
    print(f'Part 1: {sum(all(field in passport for field in part_1_required_fields) for passport in passports)}')


def height_check(passport):
    height = passport.get('hgt', '')
    if 'cm' in height:
        return 150 <= int(height[:-2]) <= 193
    if 'in' in height:
        return 59 <= int(height[:-2]) <= 76
    return False


part_2_rules = [
    lambda p: 1920 <= int(p.get('byr', 0)) <= 2002,
    lambda p: 2010 <= int(p.get('iyr', 0)) <= 2020,
    lambda p: 2020 <= int(p.get('eyr', 0)) <= 2030,
    height_check,
    lambda p: re.match(r'^#[0-9a-f]{6}$', p.get('hcl', '')),
    lambda p: p.get('ecl', '') in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'],
    lambda p: re.match(r'^[0-9]{9}$', p.get('pid', ''))
]

def part2(passports):
    print(f'Part 2: {sum(all(rule(passport) for rule in part_2_rules) for passport in passports)}')


