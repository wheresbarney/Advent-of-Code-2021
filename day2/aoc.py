#!/usr/bin/env python3.8

from collections import defaultdict
from sys import argv

def q1(moves):
    d = defaultdict(int)
    for move in moves:
        direction, magnitude = move.split(' ')
        magnitude = int(magnitude)
        d[direction] += magnitude
    return d['forward'] * (d['down'] - d['up'])

def q2(moves):
    aim = 0
    forward = 0
    depth = 0
    for move in moves:
        direction, magnitude = move.split(' ')
        magnitude = int(magnitude)
        if direction == 'forward':
            forward += magnitude
            depth += magnitude * aim
        elif direction == 'down':
            aim += magnitude
        elif direction == 'up':
            aim -= magnitude

    return forward * depth

if len(argv) > 1:
    with open(argv[1], 'r') as f:
        print(q2([l.strip() for l in f]))
else:
    print(q2([ 'forward 5','down 5','forward 8','up 3','down 8','forward 2']))
