


def parse_data(data):
    return [line for line in data.split('\n') if line]


def decode_seat(code):
    row_code = code[:7]
    col_code = code[7:]
    
    row_value = decode(0, 127, row_code)
    col_value = decode(0, 7, col_code.replace('L', 'F').replace('R', 'B'))

    return row_value, col_value


def seat_id(row, col):
    return row * 8 + col


def decode(min_v, max_v, code):
    if len(code) == 1:
        return min_v if code[0] == 'F' else max_v
    
    if code[0] == 'F':
        return decode(min_v, min_v + (max_v - min_v) // 2, code[1:])
    else:
        return decode(min_v + 1 + (max_v - min_v) // 2, max_v, code[1:])


def part1(data):
    print(f'Part 1: {max(seat_id(*decode_seat(seat)) for seat in data)}')


def part2(data):
    seat_ids = sorted(seat_id(*decode_seat(seat)) for seat in data)
    print(f'Part 2: {next(seat_id + 1 for idx, seat_id in enumerate(seat_ids) if seat_ids[idx + 1] != seat_id + 1)}')


def test(data):
    for seat in data:
        row, col = decode_seat(seat)
        print(seat, row, col, seat_id(row, col))
