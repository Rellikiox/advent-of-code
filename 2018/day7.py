
from operator import attrgetter
import sys
import re

line_regex = re.compile(
    r'Step ([a-zA-Z0-9_]+) must be finished before step ([a-zA-Z0-9_]+) can begin.'
)


class Node(object):
    def __init__(self, label, requirements):
        self.label = label.upper()
        self.requirements = [requirement.lower() for requirement in requirements]

    def requirements_met(self, problem_space):
        return all(requirement in problem_space for requirement in self.requirements)

    def is_solved(self, problem_space):
        return self.label.lower() in problem_space

    def __str__(self):
        return '{} -> {}'.format(self.requirement, self.label.upper())

    def __repr__(self):
        return str(self)


class ProblemSpace(object):
    @classmethod
    def from_input(cls, input_data):
        raw_data = {}
        total_nodes = set()
        for raw_line in input_data:
            requirement, label = line_regex.match(raw_line).groups()
            raw_data.setdefault(label, []).append(requirement)
            total_nodes.add(requirement)
        raw_data.update({
            start_node: []
            for start_node in total_nodes
            if start_node not in raw_data
        })

        node_dict = {
            _label: Node(_label, requirements)
            for _label, requirements in raw_data.iteritems()
        }
        return cls(node_dict)

    def __init__(self, nodes):
        self.nodes = nodes
        self.problem_space = sorted(node.label for node in self.nodes.values())
        self.steps_to_solve = []

    def __repr__(self):
        return ''.join(self.problem_space)

    @property
    def steps(self):
        return ''.join(self.steps_to_solve)

    def is_solved(self):
        str_problem_space = ''.join(self.problem_space)
        return str_problem_space == str_problem_space.lower()

    def solve(self):
        while not self.is_solved():
            for idx, label in enumerate(self.problem_space):
                node = self.nodes.get(label.upper())
                if (
                    not node.is_solved(self.problem_space) and
                    node.requirements_met(self.problem_space)
                ):
                    self.problem_space[idx] = label.lower()
                    self.steps_to_solve.append(label)
                    break


def solve_timed(nodes, workers, base_task_time):
    """This solution is not currently working, but I "accidentally" brute-forced the answer"""
    sorted_nodes = [
        [node.label, node.requirements, time_for_node(node.label, base_task_time), False, False]
        for node in sorted(nodes.values(), key=attrgetter('label'))
    ]
    solved_nodes = set()
    available_workers = workers
    elapsed_time = 0

    for node in sorted_nodes:
        print node[0], ''.join(node[1])
    print '    ', '   '.join(node[0] for node in sorted_nodes)
    while True:
        workers_freed = 0
        for node in sorted_nodes:
            if node[4]:  # Node is solved
                continue

            if node[3]:  # Node is being worked on
                node[2] -= 1
                if node[2] == 0:  # Node is finished
                    solved_nodes.add(node[0].lower())
                    workers_freed += 1
                    node[4] = True
            elif all(requirement in solved_nodes for requirement in node[1]):
                if available_workers > 0:
                    available_workers -= 1
                    node[2] -= 1
                    node[3] = True

        available_workers += workers_freed
        if all(node[2] == 0 for node in sorted_nodes):
            break
        print_nodes(elapsed_time, sorted_nodes)
        elapsed_time += 1

    return elapsed_time


def print_nodes(elapsed_time, nodes):
    print '%03d' % elapsed_time, '  '.join(
        ' .' if node[4] else ('%02d' % node[2] if node[3] else node[0].lower().rjust(2, ' '))
        for node in nodes
    )


def time_for_node(node_label, base_task_time):
    return base_task_time + ord(node_label.upper()) - 64


def part_1(input_filename):
    with open(input_filename) as stream:
        problem_space = ProblemSpace.from_input(stream)

    problem_space.solve()
    print 'Part 1:', problem_space.steps


def part_2(input_filename, workers, base_task_time):
    with open(input_filename) as stream:
        problem_space = ProblemSpace.from_input(stream)
        print len(problem_space.nodes)
    time_to_solve = solve_timed(problem_space.nodes, int(workers), int(base_task_time))
    print 'Part 2:', time_to_solve


if __name__ == '__main__':
    if len(sys.argv) == 2:
        part_1(sys.argv[1])
    else:
        part_2(*sys.argv[1:4])
