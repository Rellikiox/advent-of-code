
def method():
    R0 = R2 = R3 = R4 = R5 = 0
    R0 = 1
    R2_values = set()
    prev_R2 = 1
    while R2 != R0:
        R5 = R2 | 65536
        R2 = 4843319

        while True:
            R4 = R5 & 255
            R2 = (((R2 + R4) & 16777215) * 65899) & 16777215
            if 256 > R5:
                break

            R4 = 0
            while True:
                R3 = (R4 + 1) * 256
                if R3 > R5:
                    break

                R4 += 1

            R5 = R4

        if R2 in R2_values:
            import pdb; pdb.set_trace()
            print prev_R2
            return
        else:
            R2_values.add(R2)
            prev_R2 = R2
            if len(R2_values) % 100 == 0:
                print len(R2_values)
