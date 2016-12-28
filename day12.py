
test_input = """cpy 41 a
inc a
inc a
dec a
jnz a 2
dec a"""


class CPU(object):
    def __init__(self):
        self.registers = {'a': 0, 'b': 0, 'c': 1, 'd': 0}

    def run(self, cmd):
        idx_increment = 1
        if 'cpy' in cmd:
            _, value, register = cmd.split(' ')
            self.registers[register] = self.get_register_or_value(value)
        elif 'inc' in cmd:
            _, register = cmd.split(' ')
            self.registers[register] += 1
        elif 'dec' in cmd:
            _, register = cmd.split(' ')
            self.registers[register] -= 1
        elif 'jnz' in cmd:
            _, value, jmp = cmd.split(' ')
            if self.get_register_or_value(value) != 0:
                idx_increment = int(cmd[6:])
        return idx_increment

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
    print run_program(test_input)


if __name__ == '__main__':
    main()
