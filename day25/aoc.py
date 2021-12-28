#!/usr/bin/env python3.8
# https://adventofcode.com/2021/day/25

from sys import argv

SOUTH = 'v'
EAST = '>'

def parse(input):
    data = [[None for c in range(len(input[0]))] for r in range(len(input))]
    for l in range(len(input)):
        for c, char in enumerate(input[l]):
            if char != '.':
                data[l][c] = char
    return data

def next_pos(r, c, data):
    if data[r][c] == EAST:
        return (r, (c + 1) % len(data[r]))
    return ((r + 1) % len(data), c)

def cycle(direction, data):
    moves = 0
    new_data = [[None for c in range(len(data[0]))] for r in range(len(data))]
    for r in range(len(data)):
        for c, cucumber in enumerate(data[r]):
            if cucumber == direction:
                next_r, next_c = next_pos(r, c, data)
                # print(f'{direction=}: {data[r][c]}@{(r, c)} -> {data[next_r][next_c]}@{(next_r, next_c)}')
                if data[next_r][next_c]:
                    new_data[r][c] = cucumber
                else:
                    new_data[next_r][next_c] = cucumber
                    moves += 1
            elif not new_data[r][c]:
                new_data[r][c] = data[r][c]

    return (new_data, moves)

def q1(input):
    data = parse(input)
    turns = 0
    while True:
        turns += 1

        data, east_moves = cycle(EAST, data)
        data, south_moves = cycle(SOUTH, data)
        moves = east_moves + south_moves

        # print(f'  {turns}: {moves=}')
        if moves == 0:
            for r in data:
                print(''.join([c if c else '.' for c in r]))
            return turns

if len(argv) > 1:
    with open(argv[1], 'r') as f:
        print(q1([l.strip() for l in f]))
else:
    print(q1([l.strip() for l in '''
v...>>.vv>
.vv>>.vv..
>>.>v>...v
>>v>>.>.v.
v>v.vv.v..
>.>>..v...
.vv..>.>v.
v.v..>>v.v
....v..v.>
'''.splitlines()[1:]]))
