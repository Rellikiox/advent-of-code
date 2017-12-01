
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

    def __init__(self, a=0):
        self.registers = {'a': a, 'b': 0, 'c': 0, 'd': 0}

    def run(self, memory, inst_idx):
        cmd = memory[inst_idx]
        cmd_name = cmd.split(' ')[0]
        if self.lookahed_mul(memory, inst_idx):
            # print 'lookahed_mul'
            idx_increment = self.lookahed_mul(memory, inst_idx)
        else:
            # print cmd
            idx_increment = getattr(self, cmd_name)(cmd, inst_idx, memory)
        return inst_idx + (idx_increment or 1)

    def cpy(self, cmd, *args):
        _, value, register = cmd.split(' ')
        self.registers[register] = self.get_register_or_value(value)

    def inc(self, cmd, *args):
        _, register = cmd.split(' ')
        self.registers[register] += 1

    def dec(self, cmd, *args):
        _, register = cmd.split(' ')
        self.registers[register] -= 1

    def jnz(self, cmd, *args):
        _, value, jmp = cmd.split(' ')
        if self.get_register_or_value(value) != 0:
            return self.get_register_or_value(cmd[6:])

    def tgl(self, cmd, inst_idx, inst_tape):
        _, inst_dist = cmd.split(' ')
        target_idx = inst_idx + self.get_register_or_value(inst_dist)
        if target_idx < len(inst_tape):
            inst = inst_tape[target_idx]
            if inst.count(' ') == 1:
                if 'inc' in inst:
                    inst_tape[target_idx] = inst.replace('inc', 'dec')
                else:
                    inst_tape[target_idx] = 'inc' + inst[3:]
            else:
                if 'jnz' in inst:
                    inst_tape[target_idx] = inst.replace('jnz', 'cpy')
                else:
                    inst_tape[target_idx] = 'jnz' + inst[3:]

    def lookahed_mul(self, memory, inst_idx):
        if (
            memory[inst_idx] == 'cpy b c' and
            memory[inst_idx + 1] == 'inc a' and
            memory[inst_idx + 2] == 'dec c' and
            memory[inst_idx + 3] == 'jnz c -2' and
            memory[inst_idx + 4] == 'dec d' and
            memory[inst_idx + 5] == 'jnz d -5'
        ):
            self.registers['a'] += self.get_register_or_value('b') * self.get_register_or_value('d')
            self.registers['c'] = 0
            self.registers['d'] = 0
            return 5

    def get_register_or_value(self, value):
        return self.registers[value] if value in self.registers else int(value)


def run_program(input, a=7):
    cpu = CPU(a)
    memory = [line.strip() for line in input.split('\n') if line.strip()]
    idx = 0
    while idx < len(memory):
        idx = cpu.run(memory, idx)

    return cpu.registers['a']


def main():
    print run_program(test_input)


if __name__ == '__main__':
    main()
