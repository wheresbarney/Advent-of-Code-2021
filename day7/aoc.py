#!/usr/bin/env python3.8
# https://adventofcode.com/2021/day/7

from sys import argv

def costSimple(target, positions): # q1
    return sum([abs(pos - target) for pos in positions])

cache = {}
def costComplexIterativeCached(target, positions): # q2
    cost = 0
    for pos in positions:
        if (target, pos) in cache:
            cost += cache[(target, pos)]
            continue
        thisCost = sum(range(abs(pos - target)+1))
        cost += thisCost
        cache[(target, pos)] = thisCost
    return cost

def costComplexFast(target, positions): # q2
    cost = 0
    for pos in positions:
        distance = abs(pos - target)
        thisCost = int((distance / 2)) * (distance + 1)
        if distance % 2 == 1:
            thisCost += int((distance + 1) / 2)
        cost += thisCost
    return cost

def q1(positions):
    positions = [int(s) for s in positions[0].split(',')]
    best = positions[0]
    bestCost = costComplex(best, positions)
    for target in range(min(positions) + 1, max(positions) + 1): # binary search might work, and would be much faster
        thisCost = costComplexFast(target, positions)
        if thisCost < bestCost:
            bestCost = thisCost
            best = target
    print(f'{best=} {bestCost=}')
    return bestCost

if len(argv) > 1:
    with open(argv[1], 'r') as f:
        print(q1([l.strip() for l in f]))
else:
    print(q1([l.strip() for l in '''16,1,2,0,4,2,7,1,2,14'''.splitlines()]))
