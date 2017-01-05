"""
We have to create a map composed of . and ^ and its rows look like

..^^.

To generate new rows:
    - cell x.y will look at x-1.y-1, x,y-1 and x+1.y-1 (cells outside the edge default to .)
        - if the configuration is any of ^.., ^^., .^^, ..^ then that row will have a ^
        - otherwise it'll have a .

The above example expands to

..^^.
.^^^^
^^..^

after two rows.

000 no trap
001 trap
010 no trap
011 trap
100 trap
101 no trap
110 trap
111 no trap

    0 != 2
"""

from profilehooks import profile


small_input = "..^^."
small_output = """..^^.
.^^^^
^^..^"""

large_input = ".^^.^.^^^^"
large_output = """.^^.^.^^^^
^^^...^..^
^.^^.^.^^.
..^^...^^^
.^^^^.^^.^
^^..^.^^..
^^^^..^^^.
^..^^^^.^^
.^^^..^.^^
^^.^^^..^^"""


day18_input = (
    "...^^^^^..^...^...^^^^^^...^.^^^.^.^.^^.^^^....."
    "^.^^^...^^^^^^.....^.^^...^^^^^...^.^^^.^^......^^^^"
)
day18_count_after_40 = 1982
day18_count_after_400000 = 20005203


trap_configurations = ['^..', '^^.', '.^^', '..^']


class StringTrapMap(object):
    @staticmethod
    def get_trio(row, idx):
        return ''.join([
            row[sub_idx] if 0 <= sub_idx < len(row) else '.'
            for sub_idx in range(idx - 1, idx + 2)
        ])

    @staticmethod
    def n_of_safe_tiles(trap_map):
        return trap_map.count('.')


class NoHistoryMap(StringTrapMap):
    @classmethod
    def get_map(cls, row, size):
        trap_map = [row]
        while len(trap_map) < size:
            trap_map.append(cls.get_next_row(trap_map[-1]))
        return '\n'.join(trap_map)

    @classmethod
    def get_next_row(cls, prev_row):
        return ''.join([
            '^' if cls.get_trio(prev_row, idx) in trap_configurations else '.'
            for idx in range(len(prev_row))
        ])


class HistoryMap(StringTrapMap):
    @classmethod
    def get_map(cls, row, size):
        history = {}
        trap_map = [row]
        while len(trap_map) < size:
            trap_map.append(cls.get_next_row(trap_map[-1], history))
        return '\n'.join(trap_map)

    @classmethod
    def get_next_row(cls, prev_row, history):
        if prev_row not in history:
            history[prev_row] = ''.join([
                '^' if cls.get_trio(prev_row, idx) in trap_configurations else '.'
                for idx in range(len(prev_row))
            ])
        return history[prev_row]


class LessSizeHistoryMap(HistoryMap):
    @classmethod
    def get_map(cls, row, size):
        history = {}
        total_safe_tiles = 0
        row_len = len(row)
        rows = 1
        while rows < size:
            if row not in history:
                new_row = ''.join([
                    '^' if cls.get_trio(row, row_len, idx) in trap_configurations else '.'
                    for idx in range(row_len)
                ])
                n_safe_tiles = cls.n_of_safe_tiles(new_row)
                history[row] = (new_row, n_safe_tiles)
            else:
                new_row, n_safe_tiles = history[row]
            row = new_row
            total_safe_tiles += n_safe_tiles
            rows += 1
        return total_safe_tiles

    @staticmethod
    def get_trio(row, row_len, idx):
        return ''.join([
            row[sub_idx] if 0 <= sub_idx < row_len else '.'
            for sub_idx in range(idx - 1, idx + 2)
        ])


class NoTrioMap(HistoryMap):
    """Takes ~11s for 400K lines"""
    @classmethod
    def get_map(cls, row, size):
        history = {}
        total_safe_tiles = row.count('.')
        row_len = len(row)
        rows = 1
        while rows < size:
            if row not in history:
                new_row = ''
                for idx in range(row_len):
                    bit0 = row[idx - 1] if idx > 0 else '.'
                    bit2 = row[idx + 1] if idx < row_len - 1 else '.'
                    new_row += '^' if bit0 != bit2 else '.'
                n_safe_tiles = new_row.count('.')
                history[row] = (new_row, n_safe_tiles)
            else:
                new_row, n_safe_tiles = history[row]
            row = new_row
            total_safe_tiles += n_safe_tiles
            rows += 1
        return total_safe_tiles


class BinaryMap(object):
    @classmethod
    def get_map(cls, row, size):
        row_len = len(row)
        row = bin(int(row.replace('.', '0').replace('^', '1'), 2))
        history = {}
        total_trap_tiles = bin(row).count('1')
        rows = 1
        while rows < size:
            if row not in history:
                new_row = ''
                for idx in range(row_len):
                    bit0 = row[idx - 1] if idx > 0 else '.'
                    bit2 = row[idx + 1] if idx < row_len - 1 else '.'
                    new_row += '^' if bit0 != bit2 else '.'
                n_safe_tiles = new_row.count('.')
                history[row] = (new_row, n_safe_tiles)
            else:
                new_row, n_safe_tiles = history[row]
            row = new_row
            total_trap_tiles += n_safe_tiles
            rows += 1
        return (row_len * size) - total_trap_tiles


@profile(immediate=True)
def run_map(klass, row, length):
    return klass.get_map(row, length)


def main():
    print NoHistoryMap.get_map(small_input, 3)


if __name__ == '__main__':
    main()
