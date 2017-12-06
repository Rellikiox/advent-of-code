

def load_memory():
    with open('day6.input') as memory_file:
        return [int(blocks) for blocks in memory_file.read().strip().split('\t')]


def redistribute_blocks(memory):
    history = set()
    iterations = 0
    while tuple(memory) not in history:
        history.add(tuple(memory))

        bank_to_redistribute = memory.index(max(memory))
        blocks_to_redistribute = memory[bank_to_redistribute]
        memory[bank_to_redistribute] = 0

        current_index = bank_to_redistribute + 1
        while blocks_to_redistribute > 0:
            memory[current_index % len(memory)] += 1
            blocks_to_redistribute -= 1
            current_index += 1

        print memory
        iterations += 1

    print memory
    return iterations


def main():
    print redistribute_blocks(load_memory())
    # print redistribute_blocks([0, 2, 7, 0])


if __name__ == '__main__':
    main()
