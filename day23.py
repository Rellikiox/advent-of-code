
test_input = """cpy 2 a
tgl a
tgl a
tgl a
cpy 1 a
dec a
dec a"""

day12_test_input = """cpy 41 a
inc a
inc a
dec a
jnz a 2
dec a"""


class CPU(object):
    """ Reimplementation of day 12 CPU but slightly different"""

    def __init__(self):
        self.registers = {'a': 0, 'b': 0, 'c': 1, 'd': 0}

    def run(self, cmd):
        cmd_name = cmd.split(' ')[0]
        idx_increment = getattr(self, cmd_name)(cmd)
        return idx_increment or 1

    def cpy(self, cmd):
        _, value, register = cmd.split(' ')
        self.registers[register] = self.get_register_or_value(value)

    def inc(self, cmd):
        _, register = cmd.split(' ')
        self.registers[register] += 1

    def dec(self, cmd):
        _, register = cmd.split(' ')
        self.registers[register] -= 1

    def jnz(self, cmd):
        _, value, jmp = cmd.split(' ')
        if self.get_register_or_value(value) != 0:
            return int(cmd[6:])

    def get_register_or_value(self, value):
        return self.registers[value] if value in self.registers else int(value)


def run_program(input):
    cpu = CPU()
    memory = [line.strip() for line in input.split('\n') if line.strip()]
    idx = 0
    while idx < len(memory):
        idx += cpu.run(memory[idx])

    return cpu.registers['a']


def main():
    print run_program(day12_test_input)


if __name__ == '__main__':
    main()
