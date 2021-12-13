#!/usr/bin/env python3.8
# https://adventofcode.com/2021/day/12

from sys import argv


def parse(input):
    dots = {(int(c[0]), int(c[1])) for c in [l.split(',') for l in input if ',' in l]}
    folds = [(f[0], int(f[1])) for f in [f.split('=') for f in [l.split(' ')[2] for l in input if 'fold' in l]]]
    # print(f'{dots=} {folds=}')
    return dots, folds


def fold(dots, folds):
    for f in folds:
        fold = f[1]
        if f[0] == 'x':
            remove = {d for d in dots if d[0] >= fold}
            add = {(fold - (d[0] - fold), d[1]) for d in remove}
        else:
            remove = {d for d in dots if d[1] >= fold}
            add = {(d[0], fold - (d[1] - fold)) for d in remove}
        dots -= remove
        dots |= add
    return dots


def q1(input):
    dots, folds = parse(input)
    dots = fold(dots, [folds[0]])
    return len(dots)


def q2(input):
    dots, folds = parse(input)
    dots = fold(dots, folds)
    max_x = max([d[0] for d in dots])
    max_y = max([d[1] for d in dots])
    grid = [[' ' for x in range(max_x + 1)] for y in range(max_y + 1)]

    # print(f'{max_x=} {max_y=} {len(grid)=} {len(grid[1])=} {dots=}')
    for dot in dots:
        grid[dot[1]][dot[0]] = '@'
    for row in grid:
        print(''.join(row))


if len(argv) > 1:
    with open(argv[1], 'r') as f:
        print(q2([l.strip() for l in f]))
else:
    print(q2([l.strip() for l in '''6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5'''.splitlines()]))
