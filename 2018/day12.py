
import sys


def main(input_filename, target_generations):
    with open(input_filename) as stream:
        initial_state, rules = parse_input(stream)

    tape = {
        idx: state
        for idx, state in enumerate(initial_state)
    }

    for generation in xrange(1, target_generations + 1):
        new_tape = dict(tape)
        min_idx, max_idx = min(tape.keys()), max(tape.keys())
        for idx in range(min_idx - 2, max_idx + 3):
            local_state = ''.join(tape.get(local_idx, '.') for local_idx in range(idx - 2, idx + 3))
            for rule in rules:
                if rule[0] == local_state:
                    new_tape[idx] = rule[1]
                    break
            else:
                if min_idx <= idx <= max_idx:
                    new_tape[idx] = '.'

        if tape_to_str(tape) == tape_to_str(new_tape):
            prev_score = get_score(tape)
            curr_score = get_score(new_tape)
            score_diff = curr_score - prev_score
            generation_diff = target_generations - generation
            score_at_target_gen = curr_score + score_diff * generation_diff
            break

        tape = new_tape
        if generation == 20:
            score_at_gen_20 = get_score(tape)
            # print_tape(tape, generation, min(tape.keys()))

    print 'Part 1:', score_at_gen_20
    print 'Part 2:', score_at_target_gen


def get_score(tape):
    return sum(
        key
        for key, value in tape.iteritems()
        if value == '#'
    )


def tape_to_str(tape):
    return ''.join(tape[idx] for idx in sorted(tape.keys())).strip('.')


def parse_input(stream):
    lines = stream.read().split('\n')
    initial_state = lines[0].split(':')[1].strip()
    rules = [
        [part.strip() for part in line.split('=>')]
        for line in lines[2:]
        if line.strip()
    ]
    return initial_state, rules


def print_tape(tape, generation, start_index):
    print '[{}]({}){{{}}}: {}'.format(generation, start_index, get_score(tape), tape_to_str(tape))


if __name__ == '__main__':
    main(sys.argv[1], int(sys.argv[2]))
