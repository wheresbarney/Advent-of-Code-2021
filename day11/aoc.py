#!/usr/bin/env python3.8
# https://adventofcode.com/2021/day/10

from sys import argv

def q1(input):
    octopii = [[int(o) for o in l] for l in input]
    rows = len(octopii[0])
    cols = len(octopii)

    totalFlashes = 0

    for i in range(100):
    # for i in range(3):

        for r in range(rows):
            for c in range(cols):
                octopii[r][c] += 1
        # print()
        # [print(f'[{i}]: {row}') for row in octopii]

        flashed = [[0 for _ in range(cols)] for _ in range(rows)]
        anyFlashes = True
        while anyFlashes:
            anyFlashes = False
            for r in range(rows):
                for c in range(cols):
                    # print(f'  testing [{r},{c}]: {octopii[r][c]} ({flashed[r][c]})')
                    if octopii[r][c] > 9 and flashed[r][c] == 0:
                        # print(f'  flash: [{r},{c}]')
                        flashed[r][c] = 1
                        anyFlashes = True
                        totalFlashes += 1
                        for y in range (max(r - 1, 0), min(r + 2, rows)):
                            for x in range (max(c - 1, 0), min(c + 2, cols)):
                                # print(f'    bumping [{y},{x}]')
                                octopii[y][x] += 1

        for r in range(rows):
            for c in range(cols):
                if octopii[r][c] > 9:
                    octopii[r][c] = 0

        # print(f'{octopii}')
    return totalFlashes


def q2(input):
    octopii = [[int(o) for o in l] for l in input]
    rows = len(octopii[0])
    cols = len(octopii)

    i = 0
    while True:
        i += 1

        for r in range(rows):
            for c in range(cols):
                octopii[r][c] += 1
        # print()
        # [print(f'[{i}]: {row}') for row in octopii]

        flashed = [[0 for _ in range(cols)] for _ in range(rows)]
        anyFlashes = True
        while anyFlashes:
            anyFlashes = False
            for r in range(rows):
                for c in range(cols):
                    # print(f'  testing [{r},{c}]: {octopii[r][c]} ({flashed[r][c]})')
                    if octopii[r][c] > 9 and flashed[r][c] == 0:
                        # print(f'  flash: [{r},{c}]')
                        flashed[r][c] = 1
                        anyFlashes = True
                        for y in range (max(r - 1, 0), min(r + 2, rows)):
                            for x in range (max(c - 1, 0), min(c + 2, cols)):
                                # print(f'    bumping [{y},{x}]')
                                octopii[y][x] += 1

            if sum([sum(f) for f in flashed]) == rows * cols:
                return i

        for r in range(rows):
            for c in range(cols):
                if octopii[r][c] > 9:
                    octopii[r][c] = 0

        # print(f'{octopii}')


if len(argv) > 1:
    with open(argv[1], 'r') as f:
        print(q2([l.strip() for l in f]))
else:
    print(q2([l.strip() for l in '''5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526'''.splitlines()]))
