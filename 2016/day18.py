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

0b000 no trap
0b001 trap
0b010 no trap
0b011 trap
0b100 trap
0b101 no trap
0b110 trap
0b111 no trap

    n & 1 != (n >> 2) & 1
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


class NoTrioNoHistoryMap(HistoryMap):
    """Takes ~11s for 400K lines"""
    @classmethod
    def get_map(cls, row, size):
        total_safe_tiles = row.count('.')
        row_len = len(row)
        rows = 1
        while rows < size:
            new_row = ''
            for idx in range(row_len):
                bit0 = row[idx - 1] if idx > 0 else '.'
                bit2 = row[idx + 1] if idx < row_len - 1 else '.'
                new_row += '^' if bit0 != bit2 else '.'
            n_safe_tiles = new_row.count('.')

            row = new_row
            total_safe_tiles += n_safe_tiles
            rows += 1
        return total_safe_tiles


class BinaryMap(object):
    """
    Small map is
        00110
        01111
        11001

    # Getting the trio
    00110 must yield
    000 - 0b00110 >> 3 -> 4 - 1
    001 - 0b00110 >> 2 -> 3 - 1
    011 - 0b00110 >> 1 -> 2 - 1
    110 - 0b00110 >> 0 -> 1 - 1
    100 - 0b00110 << 1 -> 0 - 1

    # Getting the traps
    for each trio do bin(n & 1 != (n >> 2) & 1) to get the next row

    """

    @classmethod
    def get_map(cls, row, size):

        row_len = len(row)
        row = int(row.replace('.', '0').replace('^', '1'), 2)
        history = {}
        total_trap_tiles = bin(row).count('1')
        rows = 1
        while rows < size:
            if row not in history:

                # Do this on first since it needs left shift while the others need right shift
                shifted_bits = row << 1
                new_row = shifted_bits & 1 != (shifted_bits >> 2) & 1
                for idx in xrange(1, row_len):
                    shifted_bits = row >> (idx - 1)
                    new_row += (shifted_bits & 1 != (shifted_bits >> 2) & 1) << idx

                n_traps = bin(new_row).count('1')
                history[row] = (new_row, n_traps)

            else:
                new_row, n_traps = history[row]
            # import pdb; pdb.set_trace()
            row = new_row
            total_trap_tiles += n_traps
            rows += 1
        return (row_len * size) - total_trap_tiles


class BinaryNoHistoryMap(object):
    """
    Drop the map

    instead of a rolling mask just shif left and right and do a XOR

    row     1110001001
    rshift  0111000100
    lshift  1100010010
    xor     1011010110

    row     01111
    rshift  00111
    lshift  11110
    xor     11001

    """
    @classmethod
    def get_map(cls, row, size):
        row_len = len(row)
        mask = 2 ** row_len - 1
        row = int(row.replace('.', '0').replace('^', '1'), 2)
        total_trap_tiles = bin(row).count('1')
        for i in xrange(1, size):
            row = ((row >> 1) ^ (row << 1)) & mask
            total_trap_tiles += bin(row).count('1')

        return (row_len * size) - total_trap_tiles


class FromReddit(object):
    @staticmethod
    def get_map(start, size):
        traps = [[char=='^' for char in start]]
        for rowNum in range(1, size):
            traps.append([])
            for tileNum in range(len(traps[0])):
                if tileNum == 0:
                    tileL = False
                else:
                    tileL = traps[rowNum-1][tileNum-1]
                if tileNum == len(traps[0])-1:
                    tileR = False
                else:
                    tileR = traps[rowNum-1][tileNum+1]
                if int(tileR+tileL) == 1:
                    traps[rowNum].append(True)
                else:
                    traps[rowNum].append(False)

        safeCounts = [row.count(False) for row in traps]
        return sum(safeCounts)


class FromRedditComprehension(object):
    @staticmethod
    def get_map(start, size):
        traps = [[char == '^' for char in start]]
        for rowNum in range(1, size):
            traps.append([
                traps[-1][1] if tileNum == 0 else traps[-1][-2] if tileNum == (len(traps[0])-1) else traps[-1][tileNum-1] != traps[-1][tileNum+1]
                for tileNum in range(len(traps[0]))
            ])
        return sum([row.count(False) for row in traps])


@profile(immediate=True)
def run_map(klass, row, length):
    return klass.get_map(row, length)


def main():
    print NoHistoryMap.get_map(small_input, 3)


if __name__ == '__main__':
    main()
