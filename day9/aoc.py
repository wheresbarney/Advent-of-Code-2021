#!/usr/bin/env python3.8
# https://adventofcode.com/2021/day/9

from math import prod
from sys import argv

def isMinimum(x, y, map):
    candidate = map[y][x]
    if y != 0 and map[y-1][x] <= candidate: # up
        return False
    if y != len(map)-1 and map[y+1][x] <= candidate: # down
        return False
    if x != 0 and map[y][x-1] <= candidate: # left
        return False
    if x != len(map[0])-1 and map[y][x+1] <= candidate: # right
        return False
    return True

def findMinima(map):
    minima = []
    for y, row in enumerate(map):
        if row[0] < row[1]:
            if isMinimum(0, y, map): minima.append((0, y))
        prev = row[0]
        for x, digit in enumerate(row[1:]):
            x = x+1
            if digit < prev:
                if isMinimum(x, y, map): minima.append((x, y))
            prev = digit
    return minima

def basinSearch(x, y, visited, map, size):
    if x < 0 or y < 0 or x >= len(map[0]) or y >= len(map) or (x, y) in visited:
        return (False, size)

    visited.add((x, y))

    if map[y][x] == 9:
        return (False, size)

    size += 1

    res, size = basinSearch(x, y-1, visited, map, size) # up
    if not res:
        res, size = basinSearch(x+1, y, visited, map, size) # right
    if not res:
        res, size = basinSearch(x-1, y, visited, map, size) # left
    if not res:
        res, size = basinSearch(x, y+1, visited, map, size) # down

    return (res, size)


def basinSize(x, y, map):
    visited = set()
    (_, size) = basinSearch(x, y, visited, map, 0)
    print(f'basin at {(x, y)} {size=} ({visited=})')
    return size

def q1(input):
    map = [[int(c) for c in line] for line in input]
    minima = findMinima(map)
    # print(f'{minima=}')
    return sum([map[min[1]][min[0]] + 1 for min in minima])

def q2(input):
    map = [[int(c) for c in line] for line in input]
    minima = findMinima(map)
    basins = [basinSize(min[0], min[1], map) for min in minima]
    basins.sort()
    print(f'{basins=}')
    return prod(basins[-3:])

if len(argv) > 1:
    with open(argv[1], 'r') as f:
        print(q2([l.strip() for l in f]))
else:
    print(q2([l.strip() for l in '''2199943210
3987894921
9856789892
8767896789
9899965678'''.splitlines()]))
