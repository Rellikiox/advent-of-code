
test_input = """cpy 2 a
tgl a
tgl a
tgl a
cpy 1 a
dec a
dec a
out a"""

day25_input = """cpy a d
cpy 14 c
cpy 182 b
inc d
dec b
jnz b -2
dec c
jnz c -5
cpy d a
jnz 0 0
cpy a b
cpy 0 a
cpy 2 c
jnz b 2
jnz 1 6
dec b
dec c
jnz c -4
inc a
jnz 1 -7
cpy 2 b
jnz c 2
jnz 1 4
dec b
dec c
jnz 1 -4
jnz 0 0
out b
jnz a -19
jnz 1 -21"""

expected_output = [
    0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1,
    0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1,
    0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1,
    0, 1, 0, 1, 0, 1, 0, 1, 0, 1
]


class CPU(object):
    """ Reimplementation of day 12 CPU but slightly different"""

    def __init__(self, a=0):
        self.registers = {'a': a, 'b': 0, 'c': 0, 'd': 0}
        self.output = []

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

    def out(self, cmd, *args):
        _, value = cmd.split(' ')
        self.output.append(self.get_register_or_value(value))

        if len(self.output) == 100:
            print 'WINNER!!'

        expected = 0
        for val in self.output:
            if val != expected:
                return 1000
            expected = not expected

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
    for a in range(1, 1000):
        print a
        run_program(day25_input, a=a)


if __name__ == '__main__':
    main()
