
import re

leaf_program_re = r'^([a-z]+) \(([0-9]+)\)$'
node_program_re = r'^([a-z]+) \(([0-9]+)\) -> (.*)$'


def read_callstack():
    callstack = {}
    with open('day7.input') as callstack_file:
        for program_line in callstack_file:
            leaf_program = re.search(leaf_program_re, program_line)
            if leaf_program:
                callstack[leaf_program.group(1)] = {
                    'total_weight': int(leaf_program.group(2)),
                    'weight': int(leaf_program.group(2)),
                    'children': []
                }

            node_program = re.search(node_program_re, program_line)
            if node_program:
                callstack[node_program.group(1)] = {
                    'total_weight': 0,
                    'weight': int(node_program.group(2)),
                    'children': [s.strip() for s in node_program.group(3).split(',')]
                }

    # Calculate computed weights of each node (its weight plus the weight of its children)
    nodes_to_calculate = set(callstack)
    while nodes_to_calculate:
        node_id = nodes_to_calculate.pop()
        node = callstack[node_id]
        if all(callstack[child_id]['total_weight'] for child_id in node['children']):
            node['total_weight'] = node['weight'] + sum(
                callstack[child_id]['total_weight'] for child_id in node['children'])
        else:
            nodes_to_calculate.add(node_id)

    return callstack


def root_program(callstack):
    all_children = set([
        child
        for node, node_data in callstack.iteritems()
        for child in node_data['children']
    ])

    for node, node_data in callstack.iteritems():
        if node not in all_children:
            return node


def find_uneven_programs(nodes_to_check, callstack):
    for node_id in nodes_to_check:
        node_data = callstack[node_id]
        children_nodes = [callstack[child_id] for child_id in node_data['children']]
        weight_list = [child_data['total_weight'] for child_data in children_nodes]
        # If all the weights are the same then the set of them will have len() 1
        if len(set(weight_list)) > 1:
            uneven_node = None
            common_weight = None
            for node in children_nodes:
                if weight_list.count(node['total_weight']) == 1:
                    uneven_node = node
                    if common_weight:
                        break
                else:
                    common_weight = node['total_weight']
                    if uneven_node:
                        break

            uneven_children = [callstack[child_id] for child_id in uneven_node['children']]
            uneven_weight_list = [child_data['total_weight'] for child_data in uneven_children]
            if len(set(uneven_weight_list)) == 1:
                # If our children are even it means we're the uneven node
                fixed_weight = uneven_node['weight'] + (common_weight - uneven_node['total_weight'])
                return uneven_node, fixed_weight
            else:
                # Otherwise it means the uneven node is one of our children
                # Assemble new callstack with just our children
                return find_uneven_programs(node_data['children'], callstack)


def main():
    callstack = read_callstack()
    root = root_program(callstack)
    print 'Part 1:', root
    uneven_node, fixed_weight = find_uneven_programs(callstack.keys(), callstack)
    print 'Part 2:', fixed_weight


if __name__ == '__main__':
    main()
