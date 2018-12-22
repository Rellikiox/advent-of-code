
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
    'setr': ('R_', a_passthrough),
    'seti': ('I_', a_passthrough),
    'gtir': ('IR', greater_than),
    'gtri': ('RI', greater_than),
    'gtrr': ('RR', greater_than),
    'eqir': ('IR', equal_to),
    'eqri': ('RI', equal_to),
    'eqrr': ('RR', equal_to)
}


def to_int_values(values):
    return [int(v.strip()) for v in values]


Command = namedtuple('Command', ['opcode', 'a', 'b', 'c'])


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
    def parse_trace(trace):
        raw_before, raw_cmd, raw_after = trace.split('\n')

        registry_before = to_int_values(raw_before[9:19].split(','))
        command = Command(*to_int_values(raw_cmd.split(' ')))
        registry_after = to_int_values(raw_after[9:19].split(','))

        return registry_before, command, registry_after

    @staticmethod
    def parse_program(raw_program):
        return [
            Command(*to_int_values(raw_command.strip().split(' ')))
            for raw_command in raw_program.strip().split('\n')
            if raw_command.strip()
        ]

    @classmethod
    def default_cpu(cls):
        return cls([Operation(name, *params) for name, params in OPERATIONS.iteritems()])

    def __init__(self, operations):
        self.name_to_operations = {operation.name: operation for operation in operations}
        self.opcodes_to_operations = {}

    def run_program(self, program):
        registry = {0: 0, 1: 0, 2: 0, 3: 0}

        for command in program:
            operation = self.opcodes_to_operations[command.opcode]
            operation.run(command, registry)

        return registry

    def get_valid_operations(self, before, command, after):
        valid_operations = []
        for operation in self.name_to_operations.values():
            registry = dict(enumerate(before))
            operation.run(command, registry)
            if registry == dict(enumerate(after)):
                valid_operations.append(operation)
        return valid_operations

    def crack_opcode_names(self, valid_operations):
        opcode_names = {}
        for trace, operations in valid_operations:
            _, command, _ = trace
            name_set = {operation.name for operation in operations}
            if command.opcode in opcode_names:
                opcode_names[command.opcode] &= name_set
            else:
                opcode_names[command.opcode] = name_set

        name_of_opcodes = {}
        while any(operations for operations in opcode_names.values()):
            for opcode, operations in opcode_names.iteritems():
                if len(operations) == 1:
                    name_of_opcodes[operations.pop()] = opcode
                    break

            for opcode, operations in opcode_names.iteritems():
                opcode_names[opcode] -= set(name_of_opcodes.keys())

        self.opcodes_to_operations = {
            opcode: self.name_to_operations[name]
            for name, opcode in name_of_opcodes.iteritems()
        }


def main(input_filename):
    with open(input_filename) as stream:
        raw_traces, raw_program = stream.read().strip().split('\n\n\n')

    traces = [CPU.parse_trace(trace) for trace in raw_traces.split('\n\n') if trace]

    cpu = CPU.default_cpu()
    valid_operations = [(trace, cpu.get_valid_operations(*trace)) for trace in traces]

    more_than_3 = [(_, operations) for _, operations in valid_operations if len(operations) >= 3]
    print 'Part 1:', len(more_than_3)

    cpu.crack_opcode_names(valid_operations)
    registry = cpu.run_program(CPU.parse_program(raw_program))
    print 'Part 2:', registry.get(0)


if __name__ == '__main__':
    main(sys.argv[1])
