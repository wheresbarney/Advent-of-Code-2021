#!/usr/bin/env python3.8
# https://adventofcode.com/2021/day/5

from sys import argv
from collections import defaultdict, namedtuple

Coord = namedtuple('Coord', ['x', 'y'])
Line = namedtuple('Line', ['start', 'end'])

def parseInput(input):
    lines = []
    for line in input:
        coords = [[int(n) for n in s.split(',')] for s in line.split(' -> ')]
        lines.append(Line(Coord(coords[0][0], coords[0][1]), Coord(coords[1][0], coords[1][1])))
    return lines

def q1(input):
    lines = parseInput(input)
    lines = [line for line in lines if line.start.x == line.end.x or line.start.y == line.end.y]

    vents = defaultdict(int)
    for line in lines:
        # print(f'{line=}')
        for x in range(min(line.start.x, line.end.x), max(line.start.x, line.end.x) + 1):
            for y in range(min(line.start.y, line.end.y), max(line.start.y, line.end.y) + 1):
                # print(f'  vent at {x},{y}')
                vents[(x, y)] += 1

    hotspots = 0
    for coord, count in vents.items():
        if count > 1:
            # print(f'hotspot at {coord}')
            hotspots += 1

    return hotspots


def q2(input):
    lines = parseInput(input)
    vents = defaultdict(int)

    for line in lines:
        xStep = yStep = 0

        if line.start.x < line.end.x:
            xStep = 1
        elif line.start.x > line.end.x:
            xStep = -1

        if line.start.y < line.end.y:
            yStep = 1
        elif line.start.y > line.end.y:
            yStep = -1

        coord = line.start
        while coord != line.end:
            vents[(coord.x, coord.y)] += 1
            coord = Coord(coord.x + xStep, coord.y + yStep)
        vents[(line.end.x, line.end.y)] += 1 # and the last one
        # print(f'{line=}, x:{range(line.start.x, line.end.x + xStep, xStep)}, y:{range(line.start.y, line.end.y + yStep, yStep)}')

    hotspots = 0
    for coord, count in vents.items():
        if count > 1:
            # print(f'hotspot at {coord}')
            hotspots += 1

    return hotspots


if len(argv) > 1:
    with open(argv[1], 'r') as f:
        print(q2([l.strip() for l in f]))
else:
    print(q2([l.strip() for l in '''0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2'''.splitlines()]))
