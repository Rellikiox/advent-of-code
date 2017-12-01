from collections import namedtuple
import re


test_input = """Disc #1 has 5 positions; at time=0, it is at position 4.
Disc #2 has 2 positions; at time=0, it is at position 1."""
equation_re = r'Disc #(\d+) has (\d+) positions; at time=(\d+), it is at position (\d+)\.'


RawEquation = namedtuple('RawEquation', ['offset', 'modulo', 't_start', 'p_start'])
Equation = namedtuple('Equation', ['offset', 'modulo'])


def get_t0(input):
    equations = []
    mcm = 1
    for line in input.split('\n'):
        if line.strip():
            raw_equation = RawEquation(*map(int, re.findall(equation_re, line)[0]))
            t_offset = raw_equation.p_start - raw_equation.t_start + raw_equation.offset
            equations.append(Equation(t_offset, raw_equation.modulo))
            mcm *= raw_equation.modulo

    for i in range(mcm):
        if all((i + eq.offset) % eq.modulo == 0 for eq in equations):
            return i

    return None


def main():
    print get_t0(test_input)


if __name__ == '__main__':
    main()
