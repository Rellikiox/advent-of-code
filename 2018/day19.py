
import sys
from collections import namedtuple


def add(a, b):
    return a + b


def prod(a, b):
    return a * b


def bit_and(a, b):
    return a & b


def bit_or(a, b):
    return a | b


def a_passthrough(a, b):
    return a


def greater_than(a, b):
    return 1 if a > b else 0


def equal_to(a, b):
    return 1 if a == b else 0


OPERATIONS = {
    'addr': ('RR', add),
    'addi': ('RI', add),
    'mulr': ('RR', prod),
    'muli': ('RI', prod),
    'banr': ('RR', bit_and),
    'bani': ('RI', bit_and),
    'borr': ('RR', bit_or),
    'bori': ('RI', bit_or),
    'setr': ('RI', a_passthrough),
    'seti': ('II', a_passthrough),
    'gtir': ('IR', greater_than),
    'gtri': ('RI', greater_than),
    'gtrr': ('RR', greater_than),
    'eqir': ('IR', equal_to),
    'eqri': ('RI', equal_to),
    'eqrr': ('RR', equal_to)
}


def to_int_values(values):
    return [int(v.strip()) for v in values]


Command = namedtuple('Command', ['name', 'a', 'b', 'c'])


class Operation(object):
    def __init__(self, name, access_type, func):
        self.name = name
        self.access_type = {
            'a': access_type[0],
            'b': access_type[1],
        }
        self.func = func

    def run(self, command, registry):
        a = self.value('a', command, registry)
        b = self.value('b', command, registry)
        registry[command.c] = self.func(a, b)

    def value(self, argument, command, registry):
        argument_value = getattr(command, argument)
        if self.access_type[argument] == 'I':
            return argument_value
        else:
            return registry[argument_value]

    def __repr__(self):
        return self.name


class CPU(object):
    @staticmethod
    def parse_program(raw_program):
        ip_declaration = raw_program[0]
        ip_registry = int(ip_declaration.split(' ')[1])
        commands = []
        for raw_command in raw_program[1:]:
            if raw_command.strip():
                parts = raw_command.strip().split(' ')
                name = parts[0]
                commands.append(
                    Command(name, *to_int_values(parts[1:]))
                )

        return [ip_registry] + commands

    @classmethod
    def default_cpu(cls):
        return cls([Operation(name, *params) for name, params in OPERATIONS.iteritems()])

    def __init__(self, operations):
        self.operations = {operation.name: operation for operation in operations}

    def run_program(self, program):
        registry = {0: 1, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        ip = 0
        ip_registry, program = program[0], program[1:]
        while ip < len(program):
            command = program[ip]
            registry[ip_registry] = ip

            operation = self.operations[command.name]
            operation.run(command, registry)

            ip = registry.get(ip_registry) + 1

        return registry


def main(input_filename):
    with open(input_filename) as stream:
        raw_program = stream.read().strip().split('\n')

    cpu = CPU.default_cpu()
    registry = cpu.run_program(CPU.parse_program(raw_program))
    print 'Part 1:', registry.get(0)

    # registry = cpu.run_program(CPU.parse_program(raw_program))
    # print 'Part 2:', registry.get(0)


if __name__ == '__main__':
    main(sys.argv[1])
