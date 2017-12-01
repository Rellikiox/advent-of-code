"""
For part 1:

Lets try some examples

2 = 2 ** 1 - 0
-> 1

3 = 2 ** 2 - 1
-> 3

4 = 2 ** 2 - 0
-> 1

5 = 2 ** 3 - 3
-> 3

6 = 2 ** 3 - 2
-> 5

7 = 2 ** 3 - 1
-> 7

8 = 2 ** 3
-> 1

9 = 2 ** 4 - 7
-> 3

10 = 2 ** 4 - 6
-> 5

seems that you can do:
    - calculate the different to the next power of two
    - the number is the the one at that position from the end


For part 2:
You have to take the one across from you instead of the next one

4 = 2 ** 2
1234 - 1 234
12 4 - 2 41
12   - 1 2
1

5 = 2 ** 2 + 1
12345 - 1 2345
12 45 - 2 451
12 4  - 4 12
 2 4  - 2 4
 2

6 = 2 ** 2 + 2
123456 - 1 23456
123 56 - 2 3561
123  6 - 3 612
 23  6 - 6 23
  3  6 - 3 6
  3

7 = 2 ** 2 - 3
1234567 - 1 234567
123 567 - 2 35671
123 5 7 - 3 5712
123 5   - 5 123
1 3 5   - 1 35
1   5   - 5 1
    5


8 = 2 ** 3
12345678 - 1 2345678
1234 678 - 2 346781
1234  78 - 3 47812
1234  7  - 4 7123
 234  7  - 7 234
 2 4  7  - 2 47
 2    7  - 7 2
      7

Can't seem to find an easy way out, I'll do it the hard way

After doing it the hard way and printing numbers up to 100 it seems it
sort of follows a 3^x power. For example:

n   log3    result  index
------------------
9   2.0     9       -
10  2.1     1       1
11  2.1     2       2
12  2.2     3       3
13  2.3     4       4
14  2.4     5       5
15  2.4     6       6
16  2.5     7       7
17  2.5     8       8
18  2.6     9       9
19  2.6     11      10
20  2.7     13      11
21  2.7     15      12
22  2.8     17      13
23  2.8     19      14
24  2.8     21      15
25  2.9     23      16
26  2.9     25      17
27  3.0     27      18

so we have the following rules:
- if number is between a log3 and the mid point to the next log3 then
it's the index on that list
- if it's between the midpoint and the next log3 then it's the index since the
prev log3 times 2 minus half the distance

"""
from __future__ import division
import math


test_input = 3018458
simple_out = 1842613
complex_out = 1424135


def get_simple_last_elf(n):
    return ((n - 2 ** math.ceil(math.log(n, 2))) % n) + 1


def get_complex_last_elf_long_way(n):
    numbers = range(1, n + 1)
    idx = 0
    while len(numbers) > 1:
        numbers_len = len(numbers)
        out_index = idx + int(math.ceil((numbers_len - 1) / 2))
        prev_number = numbers[idx]
        numbers.pop(out_index % numbers_len)
        idx = (numbers.index(prev_number) + 1) % len(numbers)

    return numbers[0]


def get_complex_last_elf(n):
    """I'm sure there's a simpler way, but this is what I got"""
    if math.floor(math.log(n, 3)) == math.ceil(math.log(n, 3)):
        return n
    prev_log3 = 3 ** int(math.floor(math.log(n, 3)))
    next_log3 = prev_log3 + 1
    # print 'log3', prev_log3, next_log3
    midpoint = int((next_log3 - prev_log3) / 2)
    index = n - prev_log3
    # print 'midpoint index', midpoint
    # print 'midpoint', prev_log3 + midpoint
    # print 'index', index
    if index <= midpoint:
        # print 'it\'s the straight index'
        return index
    else:
        # print 'it\'s the index times 2 minus half the distance'
        return index * 2 - midpoint


def main():
    for i in range(9, 28):
        # print get_simple_last_elf(i)
        print i, math.log(i, 3), get_complex_last_elf(i)


if __name__ == '__main__':
    main()


