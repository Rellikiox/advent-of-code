
def checksum():
    with open('day2.input') as spreadsheet:
        checksum = 0
        for line in spreadsheet:
            values = [int(v) for v in line.split(' ') if v]
            checksum += max(values) - min(values)
        print checksum


def checkdiv():
    with open('day2.input') as spreadsheet:
        checksum = 0
        for line in spreadsheet:
            values = [int(v) for v in line.split(' ') if v]
            for a in values:
                for b in values:
                    if a != b and a % b == 0:
                        checksum += a / b
        print checksum


if __name__ == '__main__':
    checkdiv()
