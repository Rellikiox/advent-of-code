# coding: utf-8
input = 'R3, R1, R4, L4, R3, R1, R1, L3, L5, L5, L3, R1, R4, L2, L1, R3, L3, R2, R1, R1, L5, L2, L1, R2, L4, R1, L2, L4, R2, R2, L2, L4, L3, R1, R4, R3, L1, R1, L5, R4, L2, R185, L2, R4, R49, L3, L4, R5, R1, R1, L1, L1, R2, L1, L4, R4, R5, R4, L3, L5, R1, R71, L1, R1, R186, L5, L2, R5, R4, R1, L5, L2, R3, R2, R5, R5, R4, R1, R4, R2, L1, R4, L1, L4, L5, L4, R4, R5, R1, L2, L4, L1, L5, L3, L5, R2, L5, R4, L4, R3, R3, R1, R4, L1, L2, R2, L1, R4, R2, R2, R5, R2, R5, L1, R1, L4, R5, R4, R2, R4, L5, R3, R2, R5, R3, L3, L5, L4, L3, L2, L2, R3, R2, L1, L1, L5, R1, L3, R3, R4, R5, L3, L5, R1, L3, L5, L5, L2, R1, L3, L1, L3, R4, L1, R3, L2, L2, R3, R3, R4, R4, R1, L4, R1, L5'
dirs = ['N', 'W']
curr_dir = 0
dirs = [0, 0]
dirs = [0, 0, 0, 0]
input.split(', ')
for i in input.split(', '):
    new_dir = i[0]
    length = int(i[1:])
    new_dir += int(new_dir == 'R')
    dirs[new_dir] += length
    
new_dir
for i in input.split(', '):
    new_dir = i[0]
    length = int(i[1:])
    curr_dir += int(new_dir == 'R')
    dirs[new_dir] += length
    
for i in input.split(', '):
    new_dir = i[0]
    length = int(i[1:])
    curr_dir += int(new_dir == 'R')
    dirs[curr_dir] += length
    
for i in input.split(', '):
    new_dir = i[0]
    length = int(i[1:])
    curr_dir += int(new_dir == 'R')
    dirs[curr_dir%4] += length
    
dirs = [0, 0, 0, 0]
curr_dir = 0
for i in input.split(', '):
    new_dir = i[0]
    length = int(i[1:])
    curr_dir += int(new_dir == 'R')
    dirs[curr_dir%4] += length
    
dirs
pos = dirs[0] - dirs[2], dirs[1] - dirs[3]
pos
125+147
dirs = [0, 0, 0, 0]
curr_dir = 0
input = 'R2, L3'
def for i in input.split(', '):
        new_dir = i[0]
        length = int(i[1:])
        curr_dir += int(new_dir == 'R')
    
for i in input.split(', '):
        new_dir = i[0]
        length = int(i[1:])
        curr_dir += int(new_dir == 'R')
    
dirs
new_dir
length
dirs = [0, 0, 0, 0]
curr_dir = 0
for i in input.split(', '):
    new_dir = i[0]
    length = int(i[1:])
    curr_dir += int(new_dir == 'R')
    dirs[curr_dir%4] += length
    
dirs
dirs = [0, 0, 0, 0]
curr_dir = 0
for i in input.split(', '):
    new_dir = i[0]
    length = int(i[1:])
    curr_dir += 1 if new_dir == 'R' else -1
    dirs[curr_dir%4] += length
    
dirs
dirs = [0, 0, 0, 0]
curr_dir = 0
def distance(input):
    dirs = [0, 0, 0, 0]
    curr_dir = 0
    for i in input.split(', '):
        new_dir = i[0]
        length = int(i[1:])
        curr_dir += 1 if new_dir == 'R' else -1
        dirs[curr_dir%4] += length
    return dirs[0] + dirs[1] - dirs[2] - dirs[3]
distance('R2, L3')
input = 'R3, R1, R4, L4, R3, R1, R1, L3, L5, L5, L3, R1, R4, L2, L1, R3, L3, R2, R1, R1, L5, L2, L1, R2, L4, R1, L2, L4, R2, R2, L2, L4, L3, R1, R4, R3, L1, R1, L5, R4, L2, R185, L2, R4, R49, L3, L4, R5, R1, R1, L1, L1, R2, L1, L4, R4, R5, R4, L3, L5, R1, R71, L1, R1, R186, L5, L2, R5, R4, R1, L5, L2, R3, R2, R5, R5, R4, R1, R4, R2, L1, R4, L1, L4, L5, L4, R4, R5, R1, L2, L4, L1, L5, L3, L5, R2, L5, R4, L4, R3, R3, R1, R4, L1, L2, R2, L1, R4, R2, R2, R5, R2, R5, L1, R1, L4, R5, R4, R2, R4, L5, R3, R2, R5, R3, L3, L5, L4, L3, L2, L2, R3, R2, L1, L1, L5, R1, L3, R3, R4, R5, L3, L5, R1, L3, L5, L5, L2, R1, L3, L1, L3, R4, L1, R3, L2, L2, R3, R3, R4, R4, R1, L4, R1, L5'
distance(input)
distance('R2, R2, R2')
distance('R5, L5, R5, R3')
distance('R185')
distance('R185, L2, R4, R49')
distance('R1, R1, R1, R1')
distance('R1, L1, R1, L1')
distance('R1, R1, R2')
input = 'R3, R1, R4, L4, R3, R1, R1, L3, L5, L5, L3, R1, R4, L2, L1, R3, L3, R2, R1, R1, L5, L2, L1, R2, L4, R1, L2, L4, R2, R2, L2, L4, L3, R1, R4, R3, L1, R1, L5, R4, L2, R185, L2, R4, R49, L3, L4, R5, R1, R1, L1, L1, R2, L1, L4, R4, R5, R4, L3, L5, R1, R71, L1, R1, R186, L5, L2, R5, R4, R1, L5, L2, R3, R2, R5, R5, R4, R1, R4, R2, L1, R4, L1, L4, L5, L4, R4, R5, R1, L2, L4, L1, L5, L3, L5, R2, L5, R4, L4, R3, R3, R1, R4, L1, L2, R2, L1, R4, R2, R2, R5, R2, R5, L1, R1, L4, R5, R4, R2, R4, L5, R3, R2, R5, R3, L3, L5, L4, L3, L2, L2, R3, R2, L1, L1, L5, R1, L3, R3, R4, R5, L3, L5, R1, L3, L5, L5, L2, R1, L3, L1, L3, R4, L1, R3, L2, L2, R3, R3, R4, R4, R1, L4, R1, L5'
distance(input)
def distance(input):
    dirs = [0, 0, 0, 0]
    curr_dir = 0
    for i in input.split(', '):
        new_dir = i[0]
        length = int(i[1:])
        curr_dir += 1 if new_dir == 'R' else -1
        dirs[curr_dir%4] += length
    return abs(dirs[0]  - dirs[2]) + abs(dirs[1] - dirs[3])
distance(input)
def first_double(input):
    dirs = [0, 0, 0, 0]
        curr_dir = 0
    
def first_double(input):
    dirs = [0, 0, 0, 0]
    curr_dir = 0
    visited = []
    for i in input.split(', '):
        new_dir = i[0]
        length = int(i[1:])
        curr_dir += 1 if new_dir == 'R' else -1
        dirs[curr_dir%4] += length
        pos = (dirs[0]  - dirs[2], dirs[1] - dirs[3])
        if pos in visited:
            return abs(pos[0]) + abs(pos[1])
        visited.append(pos)
    return abs(dirs[0]  - dirs[2]) + abs(dirs[1] - dirs[3])
first_double('R1, R1, R1, R1')
first_double('R1, R1, L1, L1, L1')
first_double('R10, R1, L1, L1, L1')
first_double('R1, R1, R10, R1, L1, L1, L1')
input
first_double(input)
def first_double(input):
    dirs = [0, 0, 0, 0]
    curr_dir = 0
    visited = []
    for i in input.split(', '):
        new_dir = i[0]
        length = int(i[1:])
        curr_dir += 1 if new_dir == 'R' else -1
        dirs[curr_dir%4] += length
        pos = (dirs[0]  - dirs[2], dirs[1] - dirs[3])
        if '{}.{}'.format(pos[0], pos[1]) in visited:
            return abs(pos[0]) + abs(pos[1])
        visited.append('{}.{}'.format(pos[0], pos[1]))
    return abs(dirs[0]  - dirs[2]) + abs(dirs[1] - dirs[3])
first_double(input)
def first_double(input):
    dirs = [0, 0, 0, 0]
    curr_dir = 0
    visited = []
    for i in input.split(', '):
        new_dir = i[0]
        length = int(i[1:])
        curr_dir += 1 if new_dir == 'R' else -1
        dirs[curr_dir%4] += length
        pos = (dirs[0]  - dirs[2], dirs[1] - dirs[3])
        if '{}.{}'.format(pos[0], pos[1]) in visited:
            return abs(pos[0]) + abs(pos[1])
        visited.append('{}.{}'.format(pos[0], pos[1]))
    return abs(dirs[0]  - dirs[2]) + abs(dirs[1] - dirs[3])
print visited
get_ipython().magic(u'paste')
first_double(input)
first_double('R8, R4, R4, R8')
get_ipython().magic(u'paste')
first_double(input)
get_ipython().magic(u'paste')
first_double(input)
(0, 0) - (-1, -1)
range(0)
[
        (i, j)
        for i in range(prev_pos[0], pos[0])
        for j in range(prev_pos[1], pos[1])
    ]
prev_pos = (0,0)
pos = (1,0)
[
        (i, j)
        for i in range(prev_pos[0], pos[0])
        for j in range(prev_pos[1], pos[1])
    ]
i for i in range(prev_pos[0], pos[0])
[i for i in range(prev_pos[0], pos[0])]
[i for i in range(prev_pos[1], pos[1])]
[
        (i, j)
        for i in range(prev_pos[0], pos[0] + 1)
        for j in range(prev_pos[1], pos[1] + 1)
    ]
pos = (2,0)
[
        (i, j)
        for i in range(prev_pos[0], pos[0] + 1)
        for j in range(prev_pos[1], pos[1] + 1)
    ]
get_ipython().magic(u'paste')
first_double(input)
first_double('R8, R4, R4, R8')
input
get_ipython().magic(u'paste')
input
first_double('R8, R4, R4, R8')
get_ipython().magic(u'paste')
first_double('R8, R4, R4, R8')
get_ipython().magic(u'paste')
first_double('R8, R4, R4, R8')
get_ipython().magic(u'paste')
first_double('R8, R4, R4, R8')
get_ipython().magic(u'paste')
first_double('R8, R4, R4, R8')
range(2, 1)
range(2, 1, -1)
get_ipython().magic(u'paste')
range(2, 1, -1)
first_double('R8, R4, R4, R8')
range(2, 1, -1)
get_ipython().magic(u'paste')
first_double('R8, R4, R4, R8')
get_ipython().magic(u'paste')
first_double('R8, R4, R4, R8')
through((0, 0), (0, 10))
through((5, 10), (0, 10))
get_ipython().magic(u'paste')
first_double('R8, R4, R4, R8')
first_double(input)
get_ipython().magic(u'save day1mayhem.py 1-112')
