
import re

inst_re = r'([a-z]+) (dec|inc) ([-]?[0-9]+) if ([a-z]+) (<|<=|==|>=|>|!=) (-?[0-9]+)'


def check_regexp():
    with open('day8.input') as day8:
        for line in day8:
            if not re.match(inst_re, line):
                print line


def load_memory_tape():
    with open('day8.input') as day8:
        return [re.match(inst_re, line).groups() for line in day8]


def execute_program(memory, registers):
    for instruction in memory:
        if _condition_check(instruction, registers):
            _apply_action(instruction, registers)

        registers['__max'] = max(registers.get('__max', 0), maximum_register(registers))


def _condition_check(instruction, registers):
    register, conditional, value = instruction[3:]
    return eval('{} {} {}'.format(registers.get(register, 0), conditional, value))


def _apply_action(instruction, registers):
    register, action, value = instruction[:3]

    if action == 'inc':
        registers[register] = registers.get(register, 0) + int(value)
    else:
        registers[register] = registers.get(register, 0) - int(value)


def maximum_register(registers):
    return max(registers.values())


def main():
    registers = {}
    memory = load_memory_tape()

    execute_program(memory, registers)

    print registers['__max']


if __name__ == '__main__':
    main()
